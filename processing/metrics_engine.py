import pandas as pd

def calculate_pipeline_value(df, value_col='deal_value', status_col='status'):
    """Calculate total value of active deals in the pipeline."""
    if value_col not in df.columns or status_col not in df.columns:
        return 0
    # Include only 'Open' or equivalent statuses
    open_statuses = ['Open', 'Sales Qualified Leads', 'Proposal/Commercials Sent', 'Negotiations', 'Feasibility']
    active_deals = df[df[status_col].str.contains('|'.join(open_statuses), case=False, na=False)]
    return active_deals[value_col].sum()

def revenue_by_sector(df, value_col='deal_value', sector_col='normalized_sector'):
    """Calculate revenue distribution by sector."""
    if value_col not in df.columns or sector_col not in df.columns:
        return pd.Series()
    return df.groupby(sector_col)[value_col].sum().sort_values(ascending=False)

def deal_stage_distribution(df, stage_col='deal_stage'):
    """Count deals by their current stage."""
    if stage_col not in df.columns:
        # Try finding a stage column
        potential = [c for c in df.columns if 'stage' in c.lower()]
        if potential: stage_col = potential[0]
        else: return pd.Series()
    return df[stage_col].value_counts()

def work_order_completion_rate(df, status_col='execution_status'):
    """Calculate percentage of completed work orders."""
    if status_col not in df.columns:
        return 0
    total = len(df)
    if total == 0: return 0
    completed = len(df[df[status_col].str.contains('Completed|Executed', case=False, na=False)])
    return (completed / total) * 100

def detect_delayed_projects(df, end_date_col='expected_delivery', status_col='status'):
    """Find projects that are past their expected delivery date but not completed."""
    if end_date_col not in df.columns or status_col not in df.columns:
        return pd.DataFrame()
    
    today = pd.Timestamp.now()
    # Convert to datetime if not already
    df[end_date_col] = pd.to_datetime(df[end_date_col], errors='coerce')
    
    delayed = df[
        (df[end_date_col] < today) & 
        (~df[status_col].str.contains('Completed|Executed|Done', case=False, na=False))
    ]
    return delayed

def get_operational_workload(df, sector_col='normalized_sector'):
    """Calculate workload (count of active work orders) per sector."""
    if sector_col not in df.columns:
        return pd.Series()
    # Filter for active WOs
    active_wos = df[~df['execution_status'].str.contains('Completed|Executed', case=False, na=False)]
    return active_wos.groupby(sector_col).size().sort_values(ascending=False)
