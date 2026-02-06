import pandas as pd
import numpy as np

def load_and_process_data():
    """
    Loads data, cleans it, and performs initial analysis.
    Returns:
        combined_df (pd.DataFrame): Merged dataset
        dq_report (dict): Summary of data quality issues
    """
    # Load Data
    try:
        ops_df = pd.read_csv('operational_data.csv')
        surveys_df = pd.read_csv('survey_results.csv')
    except FileNotFoundError:
        return None, {"error": "Data files not found. Run data_gen.py first."}

    # Data Quality Check: Orphan Surveys
    # Surveys with encounter_ids that don't exist in ops_df
    valid_encounters = set(ops_df['encounter_id'])
    surveys_df['is_orphan'] = ~surveys_df['encounter_id'].isin(valid_encounters)
    
    orphan_count = surveys_df['is_orphan'].sum()
    orphan_pct = (orphan_count / len(surveys_df)) * 100
    
    # Merge Data (Left join to keep surveys, but we want to analyze drivers so we need ops data)
    # Using inner join for driver analysis, but keeping full survey set for response rates?
    # Let's do a left join on surveys -> ops to see what we can explain
    combined_df = pd.merge(surveys_df, ops_df, on='encounter_id', how='left')

    # Convert dates
    combined_df['response_date'] = pd.to_datetime(combined_df['response_date'])
    combined_df['encounter_date'] = pd.to_datetime(combined_df['encounter_date'])
    combined_df['month_year'] = combined_df['response_date'].dt.to_period('M').astype(str)

    # Calculate Correlations (Drivers)
    # We only want numeric drivers
    numeric_cols = ['wait_time_min', 'length_of_stay_hours', 'staffing_ratio']
    target_col = 'overall_satisfaction'
    
    correlations = {}
    if not combined_df.empty:
        # Filter for rows where we have both ops data and survey scores
        valid_data = combined_df.dropna(subset=numeric_cols + [target_col])
        if not valid_data.empty:
            for col in numeric_cols:
                corr = valid_data[col].corr(valid_data[target_col])
                correlations[col] = round(corr, 3)

    dq_report = {
        "total_surveys": len(surveys_df),
        "total_encounters": len(ops_df),
        "orphan_surveys_count": int(orphan_count),
        "orphan_surveys_pct": round(orphan_pct, 2),
        "missing_providers": int(ops_df['provider'].isna().sum()),
        "correlations": correlations
    }

    return combined_df, dq_report

if __name__ == "__main__":
    df, report = load_and_process_data()
    print("Data Quality Report:")
    print(report)
    print("\nSample Data:")
    print(df.head())
