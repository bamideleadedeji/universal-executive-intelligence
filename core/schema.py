import pandas as pd

class UniversalAuditSchema:
    """
    Standard Internal Schema for Bamidele Adedeji & Associates Audit Engine.
    Dynamically maps raw bank/POS column headers to standard analytical fields.
    """
    @staticmethod
    def validate_and_clean(df: pd.DataFrame) -> pd.DataFrame:
        clean_df = df.copy()
        clean_df['source_row'] = clean_df.index + 1
        
        # Helper function to find matching columns case-insensitively
        def find_col(candidates):
            for col in clean_df.columns:
                cleaned = str(col).strip().lower().replace("_", " ").replace("-", " ")
                if cleaned in candidates:
                    return col
            return None

        date_col = find_col(['transaction date', 'transaction_date', 'date', 'tx date', 'txn date', 'posting date'])
        narration_col = find_col(['narration', 'description', 'particulars', 'remarks', 'details'])
        debit_col = find_col(['debit', 'outflow', 'withdrawal', 'debit amount'])
        credit_col = find_col(['credit', 'inflow', 'deposit', 'credit amount'])
        balance_col = find_col(['balance', 'running balance', 'account balance'])
        ref_col = find_col(['value date', 'reference', 'ref', 'refid', 'transaction ref'])

        clean_df['transaction_date'] = pd.to_datetime(clean_df[date_col], errors='coerce') if date_col else pd.NaT
        clean_df['narration'] = clean_df[narration_col].astype(str).str.strip() if narration_col else "N/A"
        clean_df['reference'] = clean_df[ref_col].astype(str).str.strip() if ref_col else "N/A"

        for target_col, src_col in [('debit', debit_col), ('credit', credit_col), ('balance', balance_col)]:
            if src_col:
                clean_df[target_col] = (
                    clean_df[src_col].astype(str).str.replace(r'[^\d.]', '', regex=True)
                )
                clean_df[target_col] = pd.to_numeric(clean_df[target_col], errors='coerce').fillna(0.0)
            else:
                clean_df[target_col] = 0.0

        return clean_df
