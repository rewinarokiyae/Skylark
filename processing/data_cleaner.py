import pandas as pd
import numpy as np
import re

def normalize_dates(df, date_columns):
    """Convert inconsistent date formats to standard datetime objects."""
    for col in date_columns:
        if col in df.columns:
            # Drop rows with non-string/non-date types if necessary or fill with NaT
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def fill_missing_values(df):
    """Handle null values and missing numeric data."""
    # Identify numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    
    # Identify string columns
    string_cols = df.select_dtypes(include=['object']).columns
    df[string_cols] = df[string_cols].fillna("Unknown")
    
    return df

def standardize_sector_names(df, sector_col='sector'):
    """Normalize sector names to a consistent set."""
    if sector_col not in df.columns:
        # Try to find a sector column if not specified (e.g. sector/service)
        potential_cols = [c for c in df.columns if 'sector' in c.lower()]
        if potential_cols:
            sector_col = potential_cols[0]
        else:
            return df

    def clean_sector(name):
        if not name or pd.isna(name) or name == "Unknown":
            return "Other"
        name = str(name).strip().lower()
        if 'power' in name: return 'Powerline'
        if 'mining' in name: return 'Mining'
        if 'renew' in name: return 'Renewables'
        if 'rail' in name: return 'Railways'
        if 'tender' in name: return 'Tender'
        if 'dsp' in name: return 'DSP'
        if 'construct' in name: return 'Construction'
        return name.capitalize()

    df['normalized_sector'] = df[sector_col].apply(clean_sector)
    return df

def clean_financial_columns(df, columns):
    """Clean and convert financial strings to floats."""
    for col in columns:
        if col in df.columns:
            # Remove currency symbols and commas
            df[col] = df[col].astype(str).str.replace(r'[$,\s]', '', regex=True)
            # Handle empty strings resulting from cleanup
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

def detect_data_quality_issues(df):
    """Analyze data for quality issues and return a summary."""
    issues = []
    
    # Check for nulls in critical columns
    critical_cols = ['name', 'deal_value', 'expected_close_date', 'status']
    for col in critical_cols:
        if col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                issues.append(f"{null_count} entries are missing '{col}'.")
    
    # Check for inconsistent dates
    if 'expected_close_date' in df.columns:
        invalid_dates = df['expected_close_date'].isna().sum()
        if invalid_dates > 0:
            issues.append(f"{invalid_dates} entries have invalid or missing close dates.")
            
    return issues
