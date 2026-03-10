import pandas as pd

def total_pipeline_value(df):
    """Sum of all deal values in the pipeline."""
    if df.empty or 'Masked Deal value' not in df.columns:
        return 0
    return df['Masked Deal value'].sum()

def revenue_by_sector(df):
    """Breakdown of revenue (Amount) by sector from work orders."""
    if df.empty or 'Amount in Rupees (Excl of GST) (Masked)' not in df.columns or 'Unified_Sector' not in df.columns:
        return pd.Series(dtype=float)
    return df.groupby('Unified_Sector')['Amount in Rupees (Excl of GST) (Masked)'].sum().sort_values(ascending=False)

def top_clients_with_largest_deals(df, top_n=10):
    """Identify clients with the highest value deals."""
    if df.empty or 'Masked Deal value' not in df.columns:
        return pd.DataFrame()
    return df.sort_values(by='Masked Deal value', ascending=False).head(top_n)

def delayed_projects(df):
    """Find work orders where execution status is not completed/executed and past delivery date."""
    if df.empty: return df
    today = pd.Timestamp.now()
    if 'Execution Status' not in df.columns or 'Data Delivery Date' not in df.columns:
        return pd.DataFrame()
        
    delayed = df[
        (df['Execution Status'] != 'Completed') & 
        (df['Data Delivery Date'] < today)
    ]
    return delayed

def work_order_completion_rate(df):
    """Percentage of work orders marked as Completed."""
    if df.empty or 'Execution Status' not in df.columns:
        return 0
    completed = len(df[df['Execution Status'] == 'Completed'])
    return (completed / len(df)) * 100

def active_work_orders(df):
    """Count of work orders that are not yet Completed."""
    if df.empty or 'Execution Status' not in df.columns:
        return 0
    active = float(len(df[df['Execution Status'] != 'Completed']))
    return active

def work_order_status_breakdown(df):
    """Breakdown of work orders by their Execution Status."""
    if df.empty or 'Execution Status' not in df.columns:
        return pd.Series(dtype=int)
    return df['Execution Status'].value_counts()
