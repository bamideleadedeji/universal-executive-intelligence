import pandas as pd

class UniversalAuditSchema:
    """
    Standard Internal Schema for Bamidele Adedeji & Associates Audit Engine.
    Dynamically maps varying raw bank/POS column headers to standard analytical fields.
    """

    @staticmethod
    def validate_and_clean(df: pd.DataFrame) -> pd.DataFrame:
        clean_df = df.copy()
        
        # Helper function to find matching columns case-insensitively
        def find_col(candidates):
            for col in clean_df.columns:
                cleaned_header = str(col).strip().lower().replace("_", " ").replace("-", " ")
                if cleaned_header in candidates:
                    return col
            return None

        # Candidate mapping lists
        date_candidates = ['transaction date', 'transaction_date', 'date', 'tx date', 'txn date', 'posting date', 'value date']
        narration_candidates = ['narration', 'description', 'particulars', 'remarks', 'details', 'transaction details']
        debit_candidates = ['debit', 'outflow', 'withdrawal', 'debit amount', 'amount debited']
        credit_candidates = ['credit', 'inflow', 'deposit', 'credit amount', 'amount credited']
        balance_candidates = ['balance', 'running balance', 'account balance', 'book balance']
        ref_candidates = ['reference', 'ref', 'refid', 'transaction ref', 'ft reference', 'tran id']

        # Map or default columns
        date_col = find_col(date_candidates)
        narration_col = find_col(narration_candidates)
        debit_col = find_col(debit_candidates)
        credit_col = find_col(credit_candidates)
        balance_col = find_col(balance_candidates)
        ref_col = find_col(ref_candidates)

        # Standardize core columns
        clean_df['source_row'] = clean_df.index + 1
        
        if date_col:
            clean_df['transaction_date'] = pd.to_datetime(clean_df[date_col], errors='coerce')
        else:
            clean_df['transaction_date'] = pd.NaT

        clean_df['narration'] = clean_df[narration_col].astype(str).str.strip() if narration_col else "N/A"
        clean_df['reference'] = clean_df[ref_col].astype(str).str.strip() if ref_col else "N/A"

        # Numeric cleanup (strips commas, currency symbols like NGN/$, spaces)
        for col_target, col_source in [('debit', debit_col), ('credit', credit_col), ('balance', balance_col)]:
            if col_source:
                clean_df[col_target] = (
                    clean_df[col_source]
                    .astype(str)
                    .str.replace(r'[^\d.]', '', regex=True)
                )
                clean_df[col_target] = pd.to_numeric(clean_df[col_target], errors='coerce').fillna(0.0)
            else:
                clean_df[col_target] = 0.0

        return clean_df
