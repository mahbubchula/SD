"""
Export Routes
Export generated data to various formats (SPSS, Excel, CSV, SmartPLS)
"""

from fastapi import APIRouter, HTTPException, Depends, status, Response
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import io
import json
from app.routes.auth import verify_token

router = APIRouter()


class ExportRequest(BaseModel):
    data: List[Dict[str, Any]]
    format: str  # csv, excel, spss, smartpls, json
    filename: str = "survey_data"
    include_metadata: bool = True
    constructs: Dict[str, Any] = {}
    validation_results: Dict[str, Any] = {}


@router.post("/download")
async def export_data(
    request: ExportRequest,
    payload: dict = Depends(verify_token)
):
    """
    Export data in specified format - Survey-ready with all item-level data
    """
    try:
        df = pd.DataFrame(request.data)
        
        # 🔍 DEBUG: Log what we received
        print("=" * 50)
        print("BACKEND EXPORT: Received data")
        print(f"Data rows: {len(df)}")
        print(f"Data columns: {list(df.columns)}")
        print(f"Column count: {len(df.columns)}")
        print(f"Constructs received: {list(request.constructs.keys())}")
        print(f"Items in constructs:")
        for c_name, c_spec in request.constructs.items():
            if isinstance(c_spec, dict) and 'items' in c_spec:
                items = [item.get('name', '') for item in c_spec.get('items', [])]
                print(f"  {c_name}: {items}")
        print("=" * 50)
        
        # Organize columns for survey format (demographics first, then items by construct)
        df_organized = organize_dataframe_by_constructs(df, request.constructs)

        if request.format == "csv":
            return export_csv(df_organized, request.filename, request.constructs)

        elif request.format == "excel":
            return export_excel(df_organized, request.filename, request.include_metadata,
                              request.constructs, request.validation_results)

        elif request.format == "spss":
            return export_spss(df_organized, request.filename, request.constructs)

        elif request.format == "smartpls":
            return export_smartpls(df_organized, request.filename, request.constructs)

        elif request.format == "json":
            return export_json(df_organized, request.filename, request.include_metadata,
                             request.constructs, request.validation_results)

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported format: {request.format}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting data: {str(e)}"
        )


def organize_dataframe_by_constructs(df: pd.DataFrame, constructs: Dict) -> pd.DataFrame:
    """
    Organize dataframe columns to show all items grouped by construct
    Format: Demographics first, then all items organized by construct
    """
    ordered_columns = []
    demographic_columns = []
    
    # Collect demographic variables
    for col in df.columns:
        if col.startswith('DEM_'):
            demographic_columns.append(col)
    
    # Collect all construct items in order
    for construct_name, construct_spec in constructs.items():
        item_names = [item.get('name', '') for item in construct_spec.get('items', [])]
        for item_name in item_names:
            if item_name in df.columns and item_name not in ordered_columns:
                ordered_columns.append(item_name)
    
    # Combine: demographics first, then construct items
    final_order = demographic_columns + ordered_columns
    
    # Add any remaining columns
    for col in df.columns:
        if col not in final_order:
            final_order.append(col)
    
    return df[final_order]


def export_csv(df: pd.DataFrame, filename: str, constructs: Dict = None) -> Response:
    """Export to CSV with proper survey format - all item-level data"""
    # Add respondent ID
    df_export = df.copy()
    df_export.insert(0, 'RespondentID', range(1, len(df) + 1))
    
    csv_data = df_export.to_csv(index=False)

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}.csv"
        }
    )


def export_excel(
    df: pd.DataFrame,
    filename: str,
    include_metadata: bool,
    constructs: Dict,
    validation_results: Dict
) -> Response:
    """Export to Excel with multiple sheets - Survey-Style Format"""
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Data sheet - Organize by constructs for survey format
        # Reorder columns to group items by construct
        ordered_columns = []
        demographic_columns = []
        
        # First, add all construct items in order
        for construct_name, construct_spec in constructs.items():
            item_names = [item.get('name', '') for item in construct_spec.get('items', [])]
            for item_name in item_names:
                if item_name in df.columns:
                    ordered_columns.append(item_name)
        
        # Then add demographic variables
        for col in df.columns:
            if col.startswith('DEM_') and col not in ordered_columns:
                demographic_columns.append(col)
        
        # Combine: demographics first (like real surveys), then items
        final_column_order = demographic_columns + ordered_columns
        
        # Ensure all columns are included
        remaining_cols = [col for col in df.columns if col not in final_column_order]
        final_column_order.extend(remaining_cols)
        
        # Reorder dataframe
        df_ordered = df[final_column_order]
        
        # Add respondent ID as first column
        df_ordered.insert(0, 'RespondentID', range(1, len(df) + 1))
        
        # Export data
        df_ordered.to_excel(writer, sheet_name='Survey_Data', index=False)
        
        # Create a survey codebook sheet
        if constructs:
            codebook_data = []
            codebook_data.append(['SURVEY CODEBOOK', '', '', '', '', ''])
            codebook_data.append(['', '', '', '', '', ''])
            
            # Demographic variables section
            if demographic_columns:
                codebook_data.append(['DEMOGRAPHIC VARIABLES', '', '', '', '', ''])
                codebook_data.append(['Variable', 'Type', 'Description', 'Values', '', ''])
                for dem_col in demographic_columns:
                    var_name = dem_col.replace('DEM_', '')
                    unique_vals = df[dem_col].unique()
                    if len(unique_vals) <= 10:
                        values = ', '.join(map(str, sorted(unique_vals)))
                    else:
                        values = f"Range: {df[dem_col].min()} to {df[dem_col].max()}"
                    codebook_data.append([dem_col, 'Demographic', var_name, values, '', ''])
                codebook_data.append(['', '', '', '', '', ''])
            
            # Constructs and items section
            codebook_data.append(['SURVEY CONSTRUCTS AND ITEMS', '', '', '', '', ''])
            codebook_data.append(['Construct', 'Item Code', 'Item', 'Scale', 'Mean', 'SD'])
            
            for construct_name, construct_spec in constructs.items():
                items = construct_spec.get('items', [])
                for idx, item in enumerate(items, 1):
                    item_name = item.get('name', '')
                    if item_name in df.columns:
                        item_mean = df[item_name].mean()
                        item_sd = df[item_name].std()
                        item_min = df[item_name].min()
                        item_max = df[item_name].max()
                        scale_info = f"{int(item_min)}-{int(item_max)} Likert"
                        codebook_data.append([
                            construct_name if idx == 1 else '',
                            item_name,
                            f"Item {idx}",
                            scale_info,
                            f"{item_mean:.2f}",
                            f"{item_sd:.2f}"
                        ])
                codebook_data.append(['', '', '', '', '', ''])
            
            # Write codebook
            pd.DataFrame(codebook_data).to_excel(
                writer, sheet_name='Codebook', index=False, header=False
            )

        # Metadata sheet
        if include_metadata and validation_results:
            # Reliability results - Enhanced with item-level details
            reliability = validation_results.get('reliability', {})
            if reliability:
                reliability_data = []
                reliability_data.append(['RELIABILITY ANALYSIS', '', '', '', '', '', '', ''])
                reliability_data.append(['', '', '', '', '', '', '', ''])
                reliability_data.append(['Construct', 'Items', 'Cronbach α', 'Status', 'CR', 'Status', 'AVE', 'Status'])
                
                for construct, metrics in reliability.items():
                    # Count items for this construct
                    n_items = len([item for item in constructs.get(construct, {}).get('items', [])])
                    
                    alpha_val = metrics.get('cronbach_alpha', 0)
                    cr_val = metrics.get('composite_reliability', 0)
                    ave_val = metrics.get('ave', 0)
                    
                    reliability_data.append([
                        construct,
                        n_items,
                        f"{alpha_val:.3f}",
                        'Excellent' if alpha_val >= 0.9 else ('Good' if alpha_val >= 0.8 else ('Acceptable' if alpha_val >= 0.7 else 'Poor')),
                        f"{cr_val:.3f}",
                        'Pass ✓' if metrics.get('cr_acceptable', False) else 'Fail ✗',
                        f"{ave_val:.3f}",
                        'Pass ✓' if metrics.get('ave_acceptable', False) else 'Fail ✗'
                    ])
                
                # Add item-level loadings
                reliability_data.append(['', '', '', '', '', '', '', ''])
                reliability_data.append(['ITEM LOADINGS BY CONSTRUCT', '', '', '', '', '', '', ''])
                reliability_data.append(['Construct', 'Item', 'Loading', 'Status', '', '', '', ''])
                
                for construct, metrics in reliability.items():
                    loadings = metrics.get('loadings', {})
                    for item_name, loading in loadings.items():
                        reliability_data.append([
                            construct,
                            item_name,
                            f"{loading:.3f}",
                            'Excellent' if loading >= 0.7 else ('Acceptable' if loading >= 0.6 else ('Weak' if loading >= 0.5 else 'Poor')),
                            '', '', '', ''
                        ])
                
                reliability_data.append(['', '', '', '', '', '', '', ''])
                reliability_data.append(['Thresholds:', '', '', '', '', '', '', ''])
                reliability_data.append(['Cronbach α > 0.7, CR > 0.7, AVE > 0.5, Loadings > 0.7', '', '', '', '', '', '', ''])

                if reliability_data:
                    pd.DataFrame(reliability_data).to_excel(
                        writer, sheet_name='Reliability', index=False, header=False
                    )

            # Validity - HTMT
            htmt = validation_results.get('validity', {}).get('htmt', {})
            if htmt:
                htmt_data = []
                for key, value in htmt.items():
                    htmt_data.append({
                        'Construct Pair': key.replace('_vs_', ' vs '),
                        'HTMT': value.get('htmt', ''),
                        'Valid': '✓' if value.get('valid', False) else '✗'
                    })
                if htmt_data:
                    pd.DataFrame(htmt_data).to_excel(
                        writer, sheet_name='HTMT', index=False
                    )

            # Path coefficients - Enhanced with significance levels
            structural = validation_results.get('structural_model', {})
            paths = structural.get('paths', [])
            if paths:
                path_data = []
                path_data.append(['DIRECT EFFECTS (Path Coefficients)', '', '', '', '', ''])
                path_data.append(['', '', '', '', '', ''])
                path_data.append(['From Construct', 'To Construct', 'Beta (β)', 't-statistic', 'p-value', 'Significant?'])
                for path in paths:
                    sig_text = '***' if path.get('p_value', 1) < 0.001 else ('**' if path.get('p_value', 1) < 0.01 else ('*' if path.get('p_value', 1) < 0.05 else 'ns'))
                    path_data.append([
                        path.get('from', ''),
                        path.get('to', ''),
                        f"{path.get('beta', 0):.3f}",
                        f"{path.get('t_statistic', 0):.3f}",
                        f"{path.get('p_value', 1):.4f}",
                        f"{'Yes ' + sig_text if path.get('significant', False) else 'No'}"
                    ])
                path_data.append(['', '', '', '', '', ''])
                path_data.append(['*** p < 0.001, ** p < 0.01, * p < 0.05, ns = not significant', '', '', '', '', ''])
                
                pd.DataFrame(path_data).to_excel(
                    writer, sheet_name='Direct_Effects', index=False, header=False
                )

            # Indirect effects (mediation) - Enhanced with clear formatting
            indirect = structural.get('indirect_effects', [])
            if indirect:
                indirect_data = []
                indirect_data.append(['INDIRECT EFFECTS (Mediation Analysis)', '', '', '', '', '', '', ''])
                indirect_data.append(['', '', '', '', '', '', '', ''])
                indirect_data.append(['Mediation Path', 'From', 'Mediator', 'To', 'Indirect Effect', 'z-score', 'p-value', 'Significant?'])
                
                for effect in indirect:
                    sig_text = '***' if effect.get('p_value', 1) < 0.001 else ('**' if effect.get('p_value', 1) < 0.01 else ('*' if effect.get('p_value', 1) < 0.05 else 'ns'))
                    indirect_data.append([
                        effect.get('path', ''),
                        effect.get('from', ''),
                        effect.get('mediator', ''),
                        effect.get('to', ''),
                        f"{effect.get('indirect_effect', 0):.3f}",
                        f"{effect.get('z_score', 0):.3f}",
                        f"{effect.get('p_value', 1):.4f}",
                        f"{'Yes ' + sig_text if effect.get('significant', False) else 'No'}"
                    ])
                
                indirect_data.append(['', '', '', '', '', '', '', ''])
                indirect_data.append(['Interpretation:', '', '', '', '', '', '', ''])
                indirect_data.append(['- Indirect effect represents the effect transmitted through a mediator', '', '', '', '', '', '', ''])
                indirect_data.append(['- Significant indirect effects indicate meaningful mediation', '', '', '', '', '', '', ''])
                indirect_data.append(['*** p < 0.001, ** p < 0.01, * p < 0.05, ns = not significant', '', '', '', '', '', '', ''])
                
                pd.DataFrame(indirect_data).to_excel(
                    writer, sheet_name='Indirect_Effects', index=False, header=False
                )

            # Total effects - Enhanced with mediation details
            total = structural.get('total_effects', [])
            if total:
                total_data = []
                total_data.append(['TOTAL EFFECTS (Direct + Indirect)', '', '', '', '', '', '', ''])
                total_data.append(['', '', '', '', '', '', '', ''])
                total_data.append(['From', 'To', 'Mediator', 'Direct Effect', 'Indirect Effect', 'Total Effect', 'Mediation Type', 'VAF%'])
                
                for effect in total:
                    vaf = effect.get('variance_accounted_for', 0)
                    total_data.append([
                        effect.get('from', ''),
                        effect.get('to', ''),
                        effect.get('mediator', ''),
                        f"{effect.get('direct_effect', 0):.3f}",
                        f"{effect.get('indirect_effect', 0):.3f}",
                        f"{effect.get('total_effect', 0):.3f}",
                        effect.get('mediation_type', ''),
                        f"{vaf:.1f}%"
                    ])
                
                total_data.append(['', '', '', '', '', '', '', ''])
                total_data.append(['Interpretation:', '', '', '', '', '', '', ''])
                total_data.append(['- Total Effect = Direct Effect + Indirect Effect', '', '', '', '', '', '', ''])
                total_data.append(['- VAF% = Variance Accounted For by mediation', '', '', '', '', '', '', ''])
                total_data.append(['- VAF > 80%: Full mediation', '', '', '', '', '', '', ''])
                total_data.append(['- 20% < VAF < 80%: Partial mediation', '', '', '', '', '', '', ''])
                total_data.append(['- VAF < 20%: No mediation', '', '', '', '', '', '', ''])
                
                pd.DataFrame(total_data).to_excel(
                    writer, sheet_name='Total_Effects', index=False, header=False
                )

            # R-squared
            r_squared = structural.get('r_squared', {})
            if r_squared:
                r2_data = []
                for construct, metrics in r_squared.items():
                    r2_data.append({
                        'Construct': construct,
                        'R²': metrics.get('r_squared', ''),
                        'Interpretation': metrics.get('interpretation', '')
                    })
                pd.DataFrame(r2_data).to_excel(
                    writer, sheet_name='R-Squared', index=False
                )

            # Multicollinearity (VIF)
            vif = validation_results.get('multicollinearity', {})
            if vif:
                vif_data = []
                for construct, metrics in vif.items():
                    vif_data.append({
                        'Construct': construct,
                        'VIF': metrics.get('vif', ''),
                        'Acceptable': '✓' if metrics.get('acceptable', False) else '✗',
                        'Good': '✓' if metrics.get('good', False) else '✗'
                    })
                pd.DataFrame(vif_data).to_excel(
                    writer, sheet_name='VIF', index=False
                )

    output.seek(0)

    return Response(
        content=output.read(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={filename}.xlsx"
        }
    )


def export_spss(df: pd.DataFrame, filename: str, constructs: Dict = None) -> Response:
    """Export to SPSS-compatible ZIP with CSV and syntax file - Survey format"""
    import zipfile

    # Add respondent ID
    df_export = df.copy()
    df_export.insert(0, 'RespondentID', range(1, len(df) + 1))
    
    # Create CSV data
    csv_data = df_export.to_csv(index=False)

    # Create SPSS syntax for variable labels
    syntax = "* SPSS Syntax for Survey Data.\n"
    syntax += "* Generated by Advanced Survey Data Generator.\n"
    syntax += "* All item-level data included with proper construct organization.\n\n"
    syntax += f"GET DATA /TYPE=TXT\n"
    syntax += f"  /FILE='{filename}.csv'\n"
    syntax += f"  /DELCASE=LINE\n"
    syntax += f"  /DELIMITERS=\",\"\n"
    syntax += f"  /QUALIFIER='\"'\n"
    syntax += f"  /ARRANGEMENT=DELIMITED\n"
    syntax += f"  /FIRSTCASE=2\n"
    syntax += f"  /VARIABLES=\n"

    for col in df_export.columns:
        syntax += f"  {col} F8.2\n"

    syntax += ".\n\n"
    syntax += "EXECUTE.\n\n"

    # Add variable labels with construct information
    syntax += "VARIABLE LABELS\n"
    syntax += "  RespondentID 'Respondent ID'\n"
    
    # Label demographic variables
    for col in df_export.columns:
        if col.startswith('DEM_'):
            var_name = col.replace('DEM_', '')
            syntax += f"  {col} 'Demographic: {var_name}'\n"
    
    # Label construct items
    if constructs:
        for construct_name, construct_spec in constructs.items():
            items = construct_spec.get('items', [])
            for idx, item in enumerate(items, 1):
                item_name = item.get('name', '')
                if item_name in df_export.columns:
                    syntax += f"  {item_name} '{construct_name} - Item {idx}'\n"
    else:
        # Fallback if no construct info
        for col in df_export.columns:
            if not col.startswith('DEM_') and col != 'RespondentID':
                syntax += f"  {col} '{col}'\n"
    
    syntax += ".\n\n"

    # Add value labels for Likert items (assuming 1-7 scale)
    syntax += "VALUE LABELS\n"
    item_cols = [col for col in df_export.columns if not col.startswith('DEM_') and col != 'RespondentID']
    for col in item_cols:
        syntax += f"  {col}\n"
        syntax += "  1 'Strongly Disagree'\n"
        syntax += "  2 'Disagree'\n"
        syntax += "  3 'Somewhat Disagree'\n"
        syntax += "  4 'Neutral'\n"
        syntax += "  5 'Somewhat Agree'\n"
        syntax += "  6 'Agree'\n"
        syntax += "  7 'Strongly Agree'\n"
    syntax += ".\n\n"
    
    # Add construct score computation if constructs provided
    if constructs:
        syntax += "* Compute construct scores (average of items).\n"
        for construct_name, construct_spec in constructs.items():
            items = construct_spec.get('items', [])
            item_names = [item.get('name', '') for item in items if item.get('name', '') in df_export.columns]
            if item_names:
                items_str = ' '.join(item_names)
                syntax += f"COMPUTE {construct_name}_Score = MEAN({items_str}).\n"
        syntax += "EXECUTE.\n\n"

    # Add descriptive statistics commands
    syntax += "* Descriptive statistics for all items.\n"
    syntax += "DESCRIPTIVES VARIABLES="
    item_cols_limited = [col for col in df_export.columns if not col.startswith('DEM_') and col != 'RespondentID']
    syntax += " ".join(item_cols_limited[:20])  # First 20 to avoid line length
    if len(item_cols_limited) > 20:
        syntax += "\n  " + " ".join(item_cols_limited[20:])
    syntax += "\n  /STATISTICS=MEAN STDDEV MIN MAX.\n\n"

    # Add reliability analysis by construct
    if constructs:
        syntax += "* Reliability analysis by construct.\n"
        for construct_name, construct_spec in constructs.items():
            items = construct_spec.get('items', [])
            item_names = [item.get('name', '') for item in items if item.get('name', '') in df_export.columns]
            if len(item_names) >= 2:
                items_str = '\n  '.join(item_names)
                syntax += f"RELIABILITY\n"
                syntax += f"  /VARIABLES={items_str}\n"
                syntax += f"  /SCALE('{construct_name}') ALL\n"
                syntax += f"  /MODEL=ALPHA\n"
                syntax += f"  /STATISTICS=DESCRIPTIVE SCALE CORR\n"
                syntax += f"  /SUMMARY=TOTAL.\n\n"

    # Add correlation matrix command
    syntax += "* Correlation matrix for construct scores.\n"
    syntax += "CORRELATIONS\n  /VARIABLES="
    if constructs:
        construct_names = [f"{c}_Score" for c in constructs.keys()]
        syntax += " ".join(construct_names[:10])
        if len(construct_names) > 10:
            syntax += "\n  " + " ".join(construct_names[10:])
    syntax += "\n  /PRINT=TWOTAIL NOSIG\n  /MISSING=PAIRWISE.\n"

    # Create ZIP file containing both CSV and syntax
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(f'{filename}.csv', csv_data)
        zip_file.writestr(f'{filename}_syntax.sps', syntax)

        # Add README
        readme = "SPSS Export Package\n"
        readme += "===================\n\n"
        readme += "Files included:\n"
        readme += f"1. {filename}.csv - Data file\n"
        readme += f"2. {filename}_syntax.sps - SPSS syntax file\n\n"
        readme += "Instructions:\n"
        readme += "1. Open SPSS\n"
        readme += "2. Open the .sps syntax file\n"
        readme += "3. Update the FILE path if needed\n"
        readme += "4. Run the syntax to import data with labels\n"
        zip_file.writestr('README.txt', readme)

    zip_buffer.seek(0)

    # Return ZIP file
    return Response(
        content=zip_buffer.read(),
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={filename}_SPSS.zip"
        }
    )


def export_smartpls(df: pd.DataFrame, filename: str, constructs: Dict) -> Response:
    """Export to SmartPLS-compatible ZIP with CSV and model file"""
    import zipfile

    csv_data = df.to_csv(index=False)

    # Create model specification file
    model_spec = "SmartPLS 4.0 Model Specification\n"
    model_spec += "=" * 50 + "\n"
    model_spec += "Generated by Advanced Survey Data Generator\n\n"

    model_spec += "MEASUREMENT MODEL (Outer Model)\n"
    model_spec += "-" * 50 + "\n\n"

    model_spec += "Constructs and Indicators:\n\n"
    for construct_name, construct_spec in constructs.items():
        model_spec += f"Construct: {construct_name}\n"
        model_spec += f"  Mode: Reflective\n"
        model_spec += f"  Indicators:\n"
        for item in construct_spec.get('items', []):
            model_spec += f"    • {item.get('name', '')}\n"
        model_spec += "\n"

    model_spec += "\n" + "=" * 50 + "\n"
    model_spec += "INSTRUCTIONS FOR SMARTPLS 4.0\n"
    model_spec += "=" * 50 + "\n\n"

    model_spec += "1. Import Data:\n"
    model_spec += f"   - File > Import Data > {filename}.csv\n"
    model_spec += "   - Select all columns\n"
    model_spec += "   - Click Import\n\n"

    model_spec += "2. Build Model:\n"
    model_spec += "   - Create constructs (latent variables):\n"
    for construct_name in constructs.keys():
        model_spec += f"     • {construct_name}\n"
    model_spec += "\n"

    model_spec += "3. Assign Indicators:\n"
    model_spec += "   - Drag indicators to their constructs:\n"
    for construct_name, construct_spec in constructs.items():
        item_names = [item.get('name', '') for item in construct_spec.get('items', [])]
        model_spec += f"     • {construct_name}: {', '.join(item_names)}\n"
    model_spec += "\n"

    model_spec += "4. Run Analysis:\n"
    model_spec += "   - Calculate > PLS Algorithm\n"
    model_spec += "   - Calculate > Bootstrapping (for significance tests)\n"
    model_spec += "   - View results in Reports\n\n"

    model_spec += "5. Evaluate Model:\n"
    model_spec += "   - Measurement Model (Outer Model):\n"
    model_spec += "     ✓ Indicator Loadings > 0.7\n"
    model_spec += "     ✓ Cronbach's Alpha > 0.7\n"
    model_spec += "     ✓ Composite Reliability > 0.7\n"
    model_spec += "     ✓ AVE > 0.5\n"
    model_spec += "     ✓ HTMT < 0.85\n"
    model_spec += "   - Structural Model (Inner Model):\n"
    model_spec += "     ✓ Path Coefficients (significance)\n"
    model_spec += "     ✓ R² values\n"
    model_spec += "     ✓ f² effect sizes\n"
    model_spec += "     ✓ Q² predictive relevance\n"

    # Create ZIP file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(f'{filename}.csv', csv_data)
        zip_file.writestr(f'{filename}_model_guide.txt', model_spec)

        # Add quick reference
        quick_ref = "SMARTPLS QUICK REFERENCE\n"
        quick_ref += "========================\n\n"
        quick_ref += "Model Quality Criteria:\n\n"
        quick_ref += "Reliability:\n"
        quick_ref += "  • Cronbach's Alpha > 0.70\n"
        quick_ref += "  • Composite Reliability > 0.70\n"
        quick_ref += "  • AVE > 0.50\n\n"
        quick_ref += "Validity:\n"
        quick_ref += "  • Loadings > 0.70\n"
        quick_ref += "  • Cross-loadings (highest on own construct)\n"
        quick_ref += "  • Fornell-Larcker (√AVE > correlations)\n"
        quick_ref += "  • HTMT < 0.85 (conservative) or < 0.90\n\n"
        quick_ref += "Structural Model:\n"
        quick_ref += "  • R²: 0.75=substantial, 0.50=moderate, 0.25=weak\n"
        quick_ref += "  • f²: 0.35=large, 0.15=medium, 0.02=small\n"
        quick_ref += "  • Q²: > 0 indicates predictive relevance\n"
        quick_ref += "  • GoF: 0.36=large, 0.25=medium, 0.10=small\n"
        zip_file.writestr('SmartPLS_Criteria.txt', quick_ref)

    zip_buffer.seek(0)

    return Response(
        content=zip_buffer.read(),
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={filename}_SmartPLS.zip"
        }
    )


def export_json(
    df: pd.DataFrame,
    filename: str,
    include_metadata: bool,
    constructs: Dict,
    validation_results: Dict
) -> Response:
    """Export to JSON format"""
    export_data = {
        'data': df.to_dict(orient='records')
    }

    if include_metadata:
        export_data['metadata'] = {
            'constructs': constructs,
            'validation_results': validation_results,
            'sample_size': len(df),
            'variables': list(df.columns)
        }

    json_data = json.dumps(export_data, indent=2)

    return Response(
        content=json_data,
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename={filename}.json"
        }
    )


@router.get("/formats")
async def get_supported_formats(payload: dict = Depends(verify_token)):
    """Get list of supported export formats"""
    return {
        'formats': [
            {
                'name': 'CSV',
                'value': 'csv',
                'description': 'Comma-Separated Values - Universal format',
                'compatible_with': ['Excel', 'SPSS', 'R', 'Python', 'SmartPLS']
            },
            {
                'name': 'Excel',
                'value': 'excel',
                'description': 'Microsoft Excel with multiple sheets',
                'compatible_with': ['Excel', 'SPSS', 'SmartPLS'],
                'features': ['Multiple sheets', 'Metadata', 'Validation results']
            },
            {
                'name': 'SPSS',
                'value': 'spss',
                'description': 'SPSS-compatible CSV with syntax file',
                'compatible_with': ['SPSS', 'AMOS'],
                'features': ['Variable labels', 'Value labels', 'Syntax file']
            },
            {
                'name': 'SmartPLS',
                'value': 'smartpls',
                'description': 'SmartPLS-ready CSV format',
                'compatible_with': ['SmartPLS 4.0'],
                'features': ['Direct import', 'Model specification']
            },
            {
                'name': 'JSON',
                'value': 'json',
                'description': 'JSON format with full metadata',
                'compatible_with': ['R', 'Python', 'Web applications'],
                'features': ['Full metadata', 'Validation results', 'Programmatic access']
            }
        ]
    }
