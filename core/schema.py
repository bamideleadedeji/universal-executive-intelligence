import pandas as pd

class UniversalAuditSchema:
    """
    Standard Internal Schema for Bamidele Adedeji & Associates Audit Engine.
    Maps all raw client inputs to standardized analytical variables.
    """
    REQUIRED_COLUMNS = [
        'source_row',
        'transaction_date',
        'narration',
        'reference',
        'debit',
        'credit',
        'balance'
    ]

    @staticmethod
    def validate_and_clean(df: pd.DataFrame) -> pd.DataFrame:
        clean_df = df.copy()
        clean_df['source_row'] = clean_df.index + 1
        clean_df['transaction_date'] = pd.to_datetime(clean_df['transaction_date'], errors='coerce')
        clean_df['debit'] = pd.to_numeric(clean_df['debit'], errors='coerce').fillna(0.0)
        clean_df['credit'] = pd.to_numeric(clean_df['credit'], errors='coerce').fillna(0.0)
        clean_df['balance'] = pd.to_numeric(clean_df['balance'], errors='coerce').fillna(0.0)
        clean_df['narration'] = clean_df['narration'].astype(str).str.strip()
        return clean_df
