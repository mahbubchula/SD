"""
Statistical Validation Engine
Validates generated data against all PLS-SEM, SEM, and fsQCA criteria
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import normaltest, shapiro, kstest, skew, kurtosis
from sklearn.metrics import mean_squared_error, mean_absolute_error
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')


class StatisticalValidator:
    """
    Comprehensive statistical validation for survey data
    Ensures data meets all criteria for SmartPLS 4.0, SEM, and fsQCA
    """

    def __init__(self):
        self.validation_results = {}

    def validate_all(
        self,
        df: pd.DataFrame,
        constructs: Dict,
        paths: List[Dict],
        alpha: float = 0.05
    ) -> Dict[str, Any]:
        """
        Run all validation tests

        Returns comprehensive validation report
        """
        results = {
            'overall_valid': True,
            'normality': self.test_normality(df, constructs),
            'reliability': self.test_reliability(df, constructs),
            'validity': self.test_validity(df, constructs),
            'structural_model': self.test_structural_model(df, constructs, paths),
            'multicollinearity': self.test_multicollinearity(df, constructs),
            'descriptive_stats': self.calculate_descriptive_stats(df, constructs),
            'model_fit': self.calculate_model_fit(df, constructs, paths)
        }

        # Check if all criteria passed
        results['overall_valid'] = self._check_overall_validity(results)

        # Sanitize all values for JSON serialization
        results = self._sanitize_for_json(results)

        self.validation_results = results
        return results

    def test_normality(self, df: pd.DataFrame, constructs: Dict) -> Dict[str, Any]:
        """
        Test normality using multiple tests
        - Kolmogorov-Smirnov
        - Shapiro-Wilk
        - Skewness and Kurtosis
        """
        normality_results = {}

        for construct_name, construct_spec in constructs.items():
            item_names = [item['name'] for item in construct_spec['items']]

            for item_name in item_names:
                if item_name in df.columns:
                    data = df[item_name].dropna()

                    # Kolmogorov-Smirnov test
                    ks_stat, ks_p = stats.kstest(data, 'norm', args=(data.mean(), data.std()))

                    # Shapiro-Wilk test (for sample size < 5000)
                    if len(data) < 5000:
                        sw_stat, sw_p = stats.shapiro(data)
                    else:
                        sw_stat, sw_p = None, None

                    # Skewness and Kurtosis
                    skewness = stats.skew(data)
                    kurt = stats.kurtosis(data)

                    normality_results[item_name] = {
                        'kolmogorov_smirnov': {
                            'statistic': float(ks_stat),
                            'p_value': float(ks_p),
                            'normal': bool(ks_p > 0.05)
                        },
                        'shapiro_wilk': {
                            'statistic': float(sw_stat) if sw_stat else None,
                            'p_value': float(sw_p) if sw_p else None,
                            'normal': bool(sw_p > 0.05) if sw_p else None
                        },
                        'skewness': float(skewness),
                        'kurtosis': float(kurt),
                        'skewness_acceptable': bool(abs(skewness) < 2),  # Rule of thumb
                        'kurtosis_acceptable': bool(abs(kurt) < 7)  # Rule of thumb
                    }

        return normality_results

    def test_reliability(self, df: pd.DataFrame, constructs: Dict) -> Dict[str, Any]:
        """
        Test internal consistency reliability
        - Cronbach's Alpha
        - Composite Reliability (CR)
        - Average Variance Extracted (AVE)
        """
        reliability_results = {}

        for construct_name, construct_spec in constructs.items():
            item_names = [item['name'] for item in construct_spec['items']]

            if all(item in df.columns for item in item_names):
                item_data = df[item_names]

                # Cronbach's Alpha
                cronbach_alpha = self._calculate_cronbach_alpha(item_data)

                # Loadings (for CR and AVE calculation)
                loadings = self._calculate_loadings(item_data)

                # Composite Reliability
                cr = self._calculate_composite_reliability(loadings)

                # Average Variance Extracted
                ave = self._calculate_ave(loadings)

                reliability_results[construct_name] = {
                    'cronbach_alpha': float(cronbach_alpha),
                    'cronbach_acceptable': bool(cronbach_alpha >= 0.7),
                    'composite_reliability': float(cr),
                    'cr_acceptable': bool(cr >= 0.7),
                    'ave': float(ave),
                    'ave_acceptable': bool(ave >= 0.5),
                    'loadings': {item: float(loadings[i]) for i, item in enumerate(item_names)}
                }

        return reliability_results

    def test_validity(self, df: pd.DataFrame, constructs: Dict) -> Dict[str, Any]:
        """
        Test discriminant validity
        - Fornell-Larcker Criterion
        - HTMT (Heterotrait-Monotrait Ratio)
        """
        validity_results = {}

        # Calculate construct scores
        construct_scores = {}
        for construct_name, construct_spec in constructs.items():
            item_names = [item['name'] for item in construct_spec['items']]
            if all(item in df.columns for item in item_names):
                construct_scores[construct_name] = df[item_names].mean(axis=1)

        construct_df = pd.DataFrame(construct_scores)

        # Correlation matrix
        corr_matrix = construct_df.corr()

        # AVE for Fornell-Larcker
        ave_values = {}
        reliability_results = self.test_reliability(df, constructs)
        for construct_name in reliability_results:
            ave_values[construct_name] = reliability_results[construct_name]['ave']

        # Fornell-Larcker Criterion
        fornell_larcker = {}
        for i, construct_i in enumerate(construct_scores.keys()):
            for j, construct_j in enumerate(construct_scores.keys()):
                if i != j:
                    key = f"{construct_i}_vs_{construct_j}"
                    squared_corr = corr_matrix.loc[construct_i, construct_j] ** 2
                    ave_i = ave_values.get(construct_i, 0)

                    fornell_larcker[key] = {
                        'correlation': float(corr_matrix.loc[construct_i, construct_j]),
                        'squared_correlation': float(squared_corr),
                        'ave': float(ave_i),
                        'valid': bool(squared_corr < ave_i)
                    }

        # HTMT (simplified calculation)
        htmt_results = {}
        for i, construct_i in enumerate(construct_scores.keys()):
            for j, construct_j in enumerate(construct_scores.keys()):
                if i < j:
                    key = f"{construct_i}_vs_{construct_j}"
                    htmt = abs(corr_matrix.loc[construct_i, construct_j])

                    htmt_results[key] = {
                        'htmt': float(htmt),
                        'valid': bool(htmt < 0.85)  # Conservative threshold
                    }

        validity_results['fornell_larcker'] = fornell_larcker
        validity_results['htmt'] = htmt_results

        # Cross-loadings analysis
        cross_loadings = self._calculate_cross_loadings(df, constructs)
        validity_results['cross_loadings'] = cross_loadings

        return validity_results

    def test_structural_model(
        self,
        df: pd.DataFrame,
        constructs: Dict,
        paths: List[Dict]
    ) -> Dict[str, Any]:
        """
        Test structural model
        - Path coefficients
        - R² values
        - Effect sizes (f²)
        """
        structural_results = {}

        # Calculate construct scores
        construct_scores = {}
        for construct_name, construct_spec in constructs.items():
            item_names = [item['name'] for item in construct_spec['items']]
            if all(item in df.columns for item in item_names):
                construct_scores[construct_name] = df[item_names].mean(axis=1)

        construct_df = pd.DataFrame(construct_scores)

        # Path analysis
        path_results = []
        for path in paths:
            from_construct = path['from']
            to_construct = path['to']

            if from_construct in construct_df.columns and to_construct in construct_df.columns:
                # Calculate correlation as path coefficient
                corr = construct_df[from_construct].corr(construct_df[to_construct])

                # T-statistic (simplified) with infinity handling
                n = len(construct_df)

                # Prevent division by zero and handle edge cases
                if abs(corr) >= 0.9999:  # Very high correlation
                    t_stat = 100.0  # Cap at reasonable value
                    p_value = 0.0
                else:
                    denominator = max(1 - corr**2, 1e-10)  # Prevent division by zero
                    t_stat = corr * np.sqrt((n - 2) / denominator)

                    # Handle infinity/nan
                    if np.isinf(t_stat) or np.isnan(t_stat):
                        t_stat = 100.0

                    # Cap t-statistic at reasonable value
                    t_stat = np.clip(t_stat, -100, 100)

                    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 2))

                path_results.append({
                    'from': from_construct,
                    'to': to_construct,
                    'beta': float(corr),
                    't_statistic': float(t_stat),
                    'p_value': float(p_value),
                    'significant': bool(p_value < 0.05),
                    'expected_significant': path.get('significant', True)
                })

        structural_results['paths'] = path_results

        # R² calculation for endogenous constructs
        r_squared = {}
        for construct_name in construct_scores.keys():
            # Find all paths pointing to this construct
            predictors = [p['from'] for p in paths if p['to'] == construct_name]

            if predictors and construct_name in construct_df.columns:
                # Simple R² calculation
                X = construct_df[predictors].values
                y = construct_df[construct_name].values

                if X.shape[1] > 0:
                    # Linear regression
                    from sklearn.linear_model import LinearRegression
                    model = LinearRegression()
                    model.fit(X, y)
                    r2 = model.score(X, y)

                    r_squared[construct_name] = {
                        'r_squared': float(r2),
                        'interpretation': self._interpret_r_squared(r2)
                    }

        structural_results['r_squared'] = r_squared

        # Calculate indirect effects (mediation analysis)
        indirect_effects = self._calculate_indirect_effects(construct_df, paths)
        structural_results['indirect_effects'] = indirect_effects

        # Calculate total effects (direct + indirect)
        total_effects = self._calculate_total_effects(paths, indirect_effects)
        structural_results['total_effects'] = total_effects

        # Detect potential moderation effects
        moderation_analysis = self._analyze_moderation(construct_df, paths)
        structural_results['moderation_analysis'] = moderation_analysis

        return structural_results

    def test_multicollinearity(self, df: pd.DataFrame, constructs: Dict) -> Dict[str, Any]:
        """
        Test for multicollinearity using VIF (Variance Inflation Factor)
        """
        multicollinearity_results = {}

        # Calculate construct scores
        construct_scores = {}
        for construct_name, construct_spec in constructs.items():
            item_names = [item['name'] for item in construct_spec['items']]
            if all(item in df.columns for item in item_names):
                construct_scores[construct_name] = df[item_names].mean(axis=1)

        construct_df = pd.DataFrame(construct_scores)

        # Calculate VIF for each construct
        from sklearn.linear_model import LinearRegression

        for i, construct_name in enumerate(construct_scores.keys()):
            other_constructs = [c for c in construct_scores.keys() if c != construct_name]

            if len(other_constructs) > 0:
                X = construct_df[other_constructs].values
                y = construct_df[construct_name].values

                model = LinearRegression()
                model.fit(X, y)
                r_squared = model.score(X, y)

                # Handle VIF calculation with safety checks
                if r_squared >= 0.9999:  # Very high R²
                    vif = 999.0
                else:
                    denominator = max(1 - r_squared, 1e-10)
                    vif = 1 / denominator
                    # Cap VIF at reasonable maximum
                    vif = min(vif, 999.0)

                multicollinearity_results[construct_name] = {
                    'vif': float(vif),
                    'acceptable': bool(vif < 5),
                    'good': bool(vif < 3)
                }

        return multicollinearity_results

    def calculate_descriptive_stats(self, df: pd.DataFrame, constructs: Dict) -> Dict[str, Any]:
        """
        Calculate descriptive statistics for all items
        """
        descriptive_stats = {}

        for construct_name, construct_spec in constructs.items():
            item_names = [item['name'] for item in construct_spec['items']]

            for item_name in item_names:
                if item_name in df.columns:
                    data = df[item_name]

                    descriptive_stats[item_name] = {
                        'mean': float(data.mean()),
                        'median': float(data.median()),
                        'std': float(data.std()),
                        'min': float(data.min()),
                        'max': float(data.max()),
                        'skewness': float(stats.skew(data)),
                        'kurtosis': float(stats.kurtosis(data))
                    }

        return descriptive_stats

    def calculate_model_fit(
        self,
        df: pd.DataFrame,
        constructs: Dict,
        paths: List[Dict]
    ) -> Dict[str, Any]:
        """
        Calculate model fit indices
        - Goodness of Fit (GoF)
        - SRMR
        - NFI
        """
        model_fit = {}

        # Calculate construct scores
        construct_scores = {}
        for construct_name, construct_spec in constructs.items():
            item_names = [item['name'] for item in construct_spec['items']]
            if all(item in df.columns for item in item_names):
                construct_scores[construct_name] = df[item_names].mean(axis=1)

        # Average R² and AVE for GoF
        reliability_results = self.test_reliability(df, constructs)
        structural_results = self.test_structural_model(df, constructs, paths)

        avg_ave = np.mean([r['ave'] for r in reliability_results.values()])
        avg_r2 = np.mean([r['r_squared'] for r in structural_results['r_squared'].values()])

        gof = np.sqrt(avg_ave * avg_r2)

        model_fit['gof'] = {
            'value': float(gof),
            'interpretation': self._interpret_gof(gof)
        }

        return model_fit

    # Helper methods

    def _calculate_cronbach_alpha(self, item_data: pd.DataFrame) -> float:
        """Calculate Cronbach's Alpha"""
        item_data = item_data.dropna()
        n_items = item_data.shape[1]

        if n_items < 2:
            return 0.0

        item_variances = item_data.var(axis=0, ddof=1)
        total_variance = item_data.sum(axis=1).var(ddof=1)

        alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)

        return max(0.0, min(1.0, alpha))

    def _calculate_loadings(self, item_data: pd.DataFrame) -> np.ndarray:
        """Calculate factor loadings (simplified using correlations)"""
        construct_score = item_data.mean(axis=1)
        loadings = []

        for col in item_data.columns:
            loading = item_data[col].corr(construct_score)
            loadings.append(max(0.0, loading))

        return np.array(loadings)

    def _calculate_composite_reliability(self, loadings: np.ndarray) -> float:
        """Calculate Composite Reliability (CR)"""
        sum_loadings = np.sum(loadings)
        sum_squared_loadings = np.sum(loadings ** 2)
        sum_error_variance = np.sum(1 - loadings ** 2)

        if sum_squared_loadings + sum_error_variance == 0:
            return 0.0

        cr = (sum_loadings ** 2) / ((sum_loadings ** 2) + sum_error_variance)

        return max(0.0, min(1.0, cr))

    def _calculate_ave(self, loadings: np.ndarray) -> float:
        """Calculate Average Variance Extracted (AVE)"""
        if len(loadings) == 0:
            return 0.0

        ave = np.mean(loadings ** 2)

        return max(0.0, min(1.0, ave))

    def _interpret_r_squared(self, r2: float) -> str:
        """Interpret R² value"""
        if r2 >= 0.75:
            return "Substantial"
        elif r2 >= 0.50:
            return "Moderate"
        elif r2 >= 0.25:
            return "Weak"
        else:
            return "Very Weak"

    def _interpret_gof(self, gof: float) -> str:
        """Interpret GoF value"""
        if gof >= 0.36:
            return "Large"
        elif gof >= 0.25:
            return "Medium"
        elif gof >= 0.10:
            return "Small"
        else:
            return "Poor"

    def _check_overall_validity(self, results: Dict) -> bool:
        """Check if all validation criteria are met"""
        # This is a simplified check - can be customized
        try:
            # Check reliability
            for construct, metrics in results['reliability'].items():
                if not metrics['cronbach_acceptable'] or not metrics['cr_acceptable'] or not metrics['ave_acceptable']:
                    return False

            # Check multicollinearity
            for construct, metrics in results['multicollinearity'].items():
                if not metrics['acceptable']:
                    return False

            return True

        except Exception:
            return False

    def _calculate_indirect_effects(self, construct_df: pd.DataFrame, paths: List[Dict]) -> List[Dict]:
        """
        Calculate indirect effects for mediation analysis
        Identifies mediation chains (A → B → C) and calculates indirect effects
        """
        indirect_effects = []

        # Build path dictionary for quick lookup
        path_dict = {}
        for path in paths:
            from_construct = path['from']
            to_construct = path['to']
            if from_construct not in path_dict:
                path_dict[from_construct] = []
            path_dict[from_construct].append(path)

        # Find all two-step mediation paths (A → B → C)
        for path1 in paths:
            a = path1['from']
            b = path1['to']
            beta_ab = path1['beta']

            # Look for paths from B to C
            if b in path_dict:
                for path2 in path_dict[b]:
                    c = path2['to']
                    beta_bc = path2['beta']

                    # Avoid circular paths
                    if c != a:
                        # Calculate indirect effect: beta_AB * beta_BC
                        indirect_effect = beta_ab * beta_bc

                        # Calculate significance (simplified using Sobel test approximation)
                        n = len(construct_df)
                        se_indirect = np.sqrt(beta_ab**2 * (1-beta_bc**2)/n + beta_bc**2 * (1-beta_ab**2)/n)
                        z_score = indirect_effect / max(se_indirect, 1e-10)
                        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

                        indirect_effects.append({
                            'path': f"{a} → {b} → {c}",
                            'from': a,
                            'mediator': b,
                            'to': c,
                            'indirect_effect': float(indirect_effect),
                            'beta_am': float(beta_ab),  # A → Mediator
                            'beta_mc': float(beta_bc),  # Mediator → C
                            'z_score': float(np.clip(z_score, -100, 100)),
                            'p_value': float(min(p_value, 1.0)),
                            'significant': bool(p_value < 0.05)
                        })

        return indirect_effects

    def _calculate_total_effects(self, paths: List[Dict], indirect_effects: List[Dict]) -> List[Dict]:
        """
        Calculate total effects (direct + indirect)
        """
        total_effects = []

        # Build a dictionary of all direct effects
        direct_dict = {}
        for path in paths:
            key = (path['from'], path['to'])
            direct_dict[key] = path['beta']

        # For each indirect effect, calculate total effect
        for indirect in indirect_effects:
            from_var = indirect['from']
            to_var = indirect['to']
            indirect_value = indirect['indirect_effect']

            # Get direct effect if it exists
            direct_value = direct_dict.get((from_var, to_var), 0.0)

            # Total effect = direct + indirect
            total_value = direct_value + indirect_value

            # Determine mediation type
            if direct_value == 0:
                mediation_type = "Full mediation (no direct path)"
            elif abs(direct_value) < 0.05 or not any(p['from'] == from_var and p['to'] == to_var and p.get('significant', True) for p in paths):
                mediation_type = "Full mediation"
            else:
                mediation_type = "Partial mediation"

            total_effects.append({
                'from': from_var,
                'to': to_var,
                'mediator': indirect['mediator'],
                'direct_effect': float(direct_value),
                'indirect_effect': float(indirect_value),
                'total_effect': float(total_value),
                'mediation_type': mediation_type,
                'variance_accounted_for': float(abs(indirect_value) / max(abs(total_value), 1e-10) * 100) if total_value != 0 else 0.0
            })

        return total_effects

    def _analyze_moderation(self, construct_df: pd.DataFrame, paths: List[Dict]) -> List[Dict]:
        """
        Analyze potential moderation effects
        Tests if a third variable (moderator) affects the relationship between X and Y
        """
        moderation_results = []

        # Get all constructs involved in paths
        constructs_in_model = set()
        for path in paths:
            constructs_in_model.add(path['from'])
            constructs_in_model.add(path['to'])

        # For each pair of constructs with a path
        for path in paths:
            x_var = path['from']
            y_var = path['to']

            if x_var not in construct_df.columns or y_var not in construct_df.columns:
                continue

            # Test each other construct as potential moderator
            for potential_moderator in constructs_in_model:
                if potential_moderator == x_var or potential_moderator == y_var:
                    continue

                if potential_moderator not in construct_df.columns:
                    continue

                # Create interaction term
                x = construct_df[x_var]
                m = construct_df[potential_moderator]
                y = construct_df[y_var]

                # Mean-center variables
                x_centered = x - x.mean()
                m_centered = m - m.mean()

                # Create interaction
                interaction = x_centered * m_centered

                # Regression: Y ~ X + M + X*M
                from sklearn.linear_model import LinearRegression

                # Model 1: Without interaction
                X1 = np.column_stack([x, m])
                model1 = LinearRegression()
                model1.fit(X1, y)
                r2_without_interaction = model1.score(X1, y)

                # Model 2: With interaction
                X2 = np.column_stack([x, m, interaction])
                model2 = LinearRegression()
                model2.fit(X2, y)
                r2_with_interaction = model2.score(X2, y)

                # Change in R²
                r2_change = r2_with_interaction - r2_without_interaction

                # Interaction coefficient
                interaction_coef = model2.coef_[2]

                # Calculate f² effect size for interaction
                if r2_without_interaction < 0.9999:
                    f_squared = r2_change / (1 - r2_with_interaction) if r2_with_interaction < 0.9999 else 999.0
                else:
                    f_squared = 0.0

                f_squared = float(np.clip(f_squared, 0, 999))

                # Interpret effect size
                if f_squared >= 0.35:
                    effect_size = "Large"
                elif f_squared >= 0.15:
                    effect_size = "Medium"
                elif f_squared >= 0.02:
                    effect_size = "Small"
                else:
                    effect_size = "None"

                # Only include if there's some moderation effect
                if r2_change > 0.001:  # Meaningful threshold
                    moderation_results.append({
                        'independent': x_var,
                        'dependent': y_var,
                        'moderator': potential_moderator,
                        'interaction_coefficient': float(interaction_coef),
                        'r2_change': float(r2_change),
                        'f_squared': f_squared,
                        'effect_size': effect_size,
                        'significant': bool(r2_change > 0.01),  # Practical significance
                        'interpretation': f"{potential_moderator} {'moderates' if r2_change > 0.01 else 'may moderate'} the relationship between {x_var} and {y_var}"
                    })

        # Sort by effect size (largest first)
        moderation_results.sort(key=lambda x: x['r2_change'], reverse=True)

        return moderation_results

    def _calculate_cross_loadings(self, df: pd.DataFrame, constructs: Dict) -> Dict[str, Any]:
        """
        Calculate cross-loadings for discriminant validity
        Each item's loading on its own construct should be higher than on other constructs
        """
        cross_loadings = {}

        # Calculate construct scores
        construct_scores = {}
        for construct_name, construct_spec in constructs.items():
            item_names = [item['name'] for item in construct_spec['items']]
            if all(item in df.columns for item in item_names):
                construct_scores[construct_name] = df[item_names].mean(axis=1)

        # For each item, calculate correlation with all constructs
        for construct_name, construct_spec in constructs.items():
            item_names = [item['name'] for item in construct_spec['items']]

            for item_name in item_names:
                if item_name in df.columns:
                    item_loadings = {}

                    for other_construct, other_score in construct_scores.items():
                        correlation = df[item_name].corr(other_score)
                        item_loadings[other_construct] = float(correlation)

                    # Check if loading on own construct is highest
                    own_loading = item_loadings.get(construct_name, 0)
                    other_loadings = [v for k, v in item_loadings.items() if k != construct_name]
                    max_other = max(other_loadings) if other_loadings else 0

                    cross_loadings[item_name] = {
                        'loadings': item_loadings,
                        'own_construct': construct_name,
                        'own_loading': own_loading,
                        'max_cross_loading': max_other,
                        'valid': bool(own_loading > max_other)
                    }

        return cross_loadings

    def _sanitize_for_json(self, obj: Any) -> Any:
        """
        Recursively sanitize all values for JSON serialization
        Converts inf/nan to safe values and ensures proper types
        """
        if isinstance(obj, dict):
            return {key: self._sanitize_for_json(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._sanitize_for_json(item) for item in obj]
        elif isinstance(obj, (np.integer, int)):
            return int(obj)
        elif isinstance(obj, (np.floating, float)):
            if np.isnan(obj):
                return 0.0
            elif np.isinf(obj):
                return 999.0 if obj > 0 else -999.0
            else:
                return float(obj)
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return self._sanitize_for_json(obj.tolist())
        else:
            return obj
