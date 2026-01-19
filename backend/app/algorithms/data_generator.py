"""
Core Statistical Data Generation Engine
Generates statistically validated synthetic survey data with precise control over all parameters
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.linalg import cholesky
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class SurveyDataGenerator:
    """
    Advanced survey data generator with full statistical control
    """

    def __init__(self, random_seed: Optional[int] = None):
        """Initialize generator with optional random seed for reproducibility"""
        if random_seed:
            np.random.seed(random_seed)
        self.data = None
        self.correlation_matrix = None

    def generate_survey_data(
        self,
        n_samples: int,
        constructs: Dict[str, Dict],
        paths: List[Dict],
        demographic_vars: Optional[List[Dict]] = None,
        likert_scale: int = 7,
        add_noise: bool = True,
        noise_level: float = 0.05
    ) -> pd.DataFrame:
        """
        Generate complete survey dataset with all specifications

        Parameters:
        -----------
        n_samples : int
            Number of responses/samples
        constructs : dict
            Construct specifications with items and parameters
        paths : list
            Structural paths between constructs
        demographic_vars : list, optional
            Demographic variables specifications
        likert_scale : int
            Likert scale range (default 7 for 1-7)
        add_noise : bool
            Add realistic noise to data
        noise_level : float
            Level of noise (0.0 to 1.0)

        Returns:
        --------
        pd.DataFrame : Generated survey data
        """

        # Step 1: Build correlation structure from paths
        correlation_matrix, construct_order = self._build_correlation_matrix(constructs, paths)
        self.correlation_matrix = correlation_matrix

        # Step 2: Generate item-level data for all constructs
        all_items_data = {}

        for construct_name, construct_spec in constructs.items():
            items = construct_spec['items']

            for item in items:
                item_data = self._generate_item_data(
                    n_samples=n_samples,
                    mean=item.get('mean', 4.0),
                    std=item.get('std', 1.0),
                    skewness=item.get('skewness', 0.0),
                    kurtosis=item.get('kurtosis', 0.0),
                    likert_scale=likert_scale
                )
                all_items_data[item['name']] = item_data

        # Step 3: Apply structural relationships (paths)
        df = pd.DataFrame(all_items_data)
        df = self._apply_structural_model(df, constructs, paths, construct_order)

        # Step 4: Add noise for realism
        if add_noise and noise_level > 0:
            df = self._add_realistic_noise(df, noise_level, likert_scale)

        # Step 5: Ensure Likert scale boundaries
        item_columns = [col for col in df.columns if not col.startswith('DEM_')]
        df[item_columns] = df[item_columns].clip(1, likert_scale)

        # Step 6: Add demographic variables
        if demographic_vars:
            df = self._add_demographic_variables(df, demographic_vars, n_samples)

        # Step 7: Round to nearest integer for Likert items
        df[item_columns] = df[item_columns].round().astype(int)

        self.data = df
        return df

    def _generate_item_data(
        self,
        n_samples: int,
        mean: float,
        std: float,
        skewness: float,
        kurtosis: float,
        likert_scale: int
    ) -> np.ndarray:
        """
        Generate data for a single item with specified distribution parameters
        Uses Fleishman's power method for non-normal distributions
        """

        if abs(skewness) < 0.01 and abs(kurtosis) < 0.01:
            # Normal distribution
            data = np.random.normal(mean, std, n_samples)
        else:
            # Non-normal distribution using power transformation
            # Generate standard normal
            z = np.random.normal(0, 1, n_samples)

            # Apply power transformation for skewness and kurtosis
            # Fleishman's method coefficients (simplified)
            a, b, c, d = self._fleishman_coefficients(skewness, kurtosis)

            # Transform
            x = a + b*z + c*z**2 + d*z**3

            # Scale to desired mean and std
            x = (x - np.mean(x)) / np.std(x) * std + mean

            data = x

        # Clip to reasonable range before Likert conversion
        data = np.clip(data, 1, likert_scale)

        return data

    def _fleishman_coefficients(
        self,
        skewness: float,
        kurtosis: float
    ) -> Tuple[float, float, float, float]:
        """
        Calculate Fleishman's power method coefficients for given skewness and kurtosis
        Simplified version for reasonable ranges
        """
        # For small skewness and kurtosis, use approximations
        c = skewness / 6.0
        d = kurtosis / 24.0
        b = np.sqrt(1 - c**2 - d**2)
        a = 0

        return a, b, c, d

    def _build_correlation_matrix(
        self,
        constructs: Dict,
        paths: List[Dict]
    ) -> Tuple[np.ndarray, List[str]]:
        """
        Build correlation matrix from structural paths
        """
        construct_names = list(constructs.keys())
        n_constructs = len(construct_names)

        # Initialize correlation matrix
        corr_matrix = np.eye(n_constructs)

        # Fill in correlations from paths
        for path in paths:
            from_idx = construct_names.index(path['from'])
            to_idx = construct_names.index(path['to'])

            # Use path coefficient as correlation
            beta = path.get('beta', 0.3)
            corr_matrix[from_idx, to_idx] = beta
            corr_matrix[to_idx, from_idx] = beta  # Symmetric

        # Ensure positive definite
        corr_matrix = self._nearest_positive_definite(corr_matrix)

        return corr_matrix, construct_names

    def _nearest_positive_definite(self, A: np.ndarray) -> np.ndarray:
        """
        Find the nearest positive definite matrix to input matrix
        """
        B = (A + A.T) / 2
        _, s, V = np.linalg.svd(B)

        H = np.dot(V.T, np.dot(np.diag(s), V))
        A2 = (B + H) / 2
        A3 = (A2 + A2.T) / 2

        if self._is_positive_definite(A3):
            return A3

        spacing = np.spacing(np.linalg.norm(A))
        I = np.eye(A.shape[0])
        k = 1
        while not self._is_positive_definite(A3):
            mineig = np.min(np.real(np.linalg.eigvals(A3)))
            A3 += I * (-mineig * k**2 + spacing)
            k += 1

        return A3

    def _is_positive_definite(self, B: np.ndarray) -> bool:
        """Check if matrix is positive definite"""
        try:
            _ = np.linalg.cholesky(B)
            return True
        except np.linalg.LinAlgError:
            return False

    def _apply_structural_model(
        self,
        df: pd.DataFrame,
        constructs: Dict,
        paths: List[Dict],
        construct_order: List[str]
    ) -> pd.DataFrame:
        """
        Apply structural relationships between constructs
        """
        # Calculate construct scores (average of items)
        construct_scores = {}
        for construct_name, construct_spec in constructs.items():
            item_names = [item['name'] for item in construct_spec['items']]
            construct_scores[construct_name] = df[item_names].mean(axis=1)

        # Apply path relationships
        for path in paths:
            from_construct = path['from']
            to_construct = path['to']
            beta = path.get('beta', 0.3)
            is_significant = path.get('significant', True)

            if not is_significant:
                beta = beta * 0.1  # Make non-significant

            # Get items of target construct
            to_items = [item['name'] for item in constructs[to_construct]['items']]

            # Apply influence
            from_scores = construct_scores[from_construct]

            for item in to_items:
                # Add effect while preserving item characteristics
                effect = beta * from_scores
                df[item] = df[item] * 0.7 + effect * 0.3

        return df

    def _add_realistic_noise(
        self,
        df: pd.DataFrame,
        noise_level: float,
        likert_scale: int
    ) -> pd.DataFrame:
        """
        Add realistic noise to simulate human response variability
        """
        item_columns = [col for col in df.columns if not col.startswith('DEM_')]

        for col in item_columns:
            noise = np.random.normal(0, noise_level * likert_scale, len(df))
            df[col] = df[col] + noise

        return df

    def _add_demographic_variables(
        self,
        df: pd.DataFrame,
        demographic_vars: List[Dict],
        n_samples: int
    ) -> pd.DataFrame:
        """
        Add demographic variables with logical generation
        """
        for demo_var in demographic_vars:
            var_name = demo_var['name']
            var_type = demo_var['type']

            if var_type == 'categorical':
                # Categorical variable (e.g., Gender, Education)
                categories = demo_var['categories']
                probabilities = demo_var.get('probabilities', None)

                if probabilities is None:
                    probabilities = [1/len(categories)] * len(categories)

                df[f'DEM_{var_name}'] = np.random.choice(
                    categories,
                    size=n_samples,
                    p=probabilities
                )

            elif var_type == 'numerical':
                # Numerical variable (e.g., Age, Income)
                min_val = demo_var.get('min', 18)
                max_val = demo_var.get('max', 65)
                mean_val = demo_var.get('mean', (min_val + max_val) / 2)
                std_val = demo_var.get('std', (max_val - min_val) / 6)

                data = np.random.normal(mean_val, std_val, n_samples)
                data = np.clip(data, min_val, max_val)
                df[f'DEM_{var_name}'] = data.round().astype(int)

            elif var_type == 'ordinal':
                # Ordinal variable (e.g., Income brackets)
                levels = demo_var['levels']
                probabilities = demo_var.get('probabilities', None)

                if probabilities is None:
                    probabilities = [1/len(levels)] * len(levels)

                df[f'DEM_{var_name}'] = np.random.choice(
                    range(1, len(levels) + 1),
                    size=n_samples,
                    p=probabilities
                )

        return df

    def calculate_construct_scores(self, df: pd.DataFrame, constructs: Dict) -> pd.DataFrame:
        """Calculate construct scores from item scores"""
        construct_df = pd.DataFrame()

        for construct_name, construct_spec in constructs.items():
            item_names = [item['name'] for item in construct_spec['items']]
            if all(item in df.columns for item in item_names):
                construct_df[construct_name] = df[item_names].mean(axis=1)

        return construct_df
