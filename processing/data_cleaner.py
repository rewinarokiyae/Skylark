import pandas as pd
import numpy as np
import re

def clean_deals_data(df):
    """Clean data specifically for the Deals board."""
    if df.empty: return df
    
    # Financial cleanup
    if 'Masked Deal value' in df.columns:
        df = clean_financial_columns(df, ['Masked Deal value'])
    
    # Date cleanup
    date_cols = ['Close Date (A)', 'Tentative Close Date', 'Created Date']
    df = normalize_dates(df, [c for c in date_cols if c in df.columns])
        
    # Standardize sector
    if 'Sector/service' in df.columns:
        df = standardize_sector_names(df, sector_col='Sector/service')
        df['Unified_Sector'] = df['normalized_sector']
        
    # Unify identities
    if 'Client Code' in df.columns:
        df['Unified_Client_Code'] = df['Client Code'].astype(str).str.strip()
    if 'Owner code' in df.columns:
        df['Unified_Owner_Code'] = df['Owner code'].astype(str).str.strip()
        
    return fill_missing_values(df)

def clean_work_orders_data(df):
    """Clean data specifically for the Work Orders board."""
    if df.empty: return df
    
    # Financial cleanup
    financial_cols = ['Amount in Rupees (Excl of GST) (Masked)', 'Amount in Rupees (Incl of GST) (Masked)']
    df = clean_financial_columns(df, [c for c in financial_cols if c in df.columns])
        
    # Date cleanup
    date_cols = ['Data Delivery Date', 'Date of PO/LOI', 'Probable Start Date', 'Probable End Date', 'Last invoice date']
    df = normalize_dates(df, [c for c in date_cols if c in df.columns])
        
    # Standardize sector
    if 'Sector' in df.columns:
        df = standardize_sector_names(df, sector_col='Sector')
        df['Unified_Sector'] = df['normalized_sector']
        
    # Unify identities
    if 'Customer Name Code' in df.columns:
        df['Unified_Client_Code'] = df['Customer Name Code'].astype(str).str.strip()
    if 'BD/KAM Personnel code' in df.columns:
        df['Unified_Owner_Code'] = df['BD/KAM Personnel code'].astype(str).str.strip()
        
    return fill_missing_values(df)

def normalize_dates(df, date_columns):
    """Convert inconsistent date formats to standard datetime objects."""
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
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

def standardize_sector_names(df, sector_col='Sector'):
    """Normalize sector names to a consistent set."""
    if sector_col not in df.columns:
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
            # Remove ₹, currency symbols and commas
            df[col] = df[col].astype(str).str.replace(r'[₹$,\s]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df
