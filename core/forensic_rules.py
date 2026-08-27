import pandas as pd

class ForensicRuleEngine:
    """
    Executes explicit statutory audits against CBN Tariff Guidelines and Duplicate Logic.
    """
    
    @staticmethod
    def audit_sms_charges(df: pd.DataFrame, max_allowed_sms_rate: float = 4.00) -> pd.DataFrame:
        """Flags SMS notification fees exceeding the CBN cap of N4.00 per SMS."""
        sms_mask = df['narration'].str.contains('SMS', case=False, na=False) & (df['debit'] > 0)
        sms_df = df[sms_mask].copy()
        
        if not sms_df.empty:
            sms_df['allowed_fee'] = max_allowed_sms_rate
            sms_df['recoverable_variance'] = sms_df['debit'].apply(lambda x: max(0.0, x - max_allowed_sms_rate))
            sms_df['violation_type'] = 'Excess SMS Notification Fee'
            sms_df['rule_reference'] = 'CBN Guide to Bank Charges (Sec 10.3)'
            return sms_df[sms_df['recoverable_variance'] > 0]
        return pd.DataFrame()

    @staticmethod
    def audit_duplicate_debits(df: pd.DataFrame) -> pd.DataFrame:
        """Identifies duplicate outflow transactions occurring on the same date with identical amounts."""
        debits = df[df['debit'] > 0].copy()
        debits['tx_date_only'] = debits['transaction_date'].dt.date
        
        duplicates = debits[debits.duplicated(subset=['tx_date_only', 'debit', 'narration'], keep=False)].copy()
        if not duplicates.empty:
            duplicates['allowed_fee'] = 0.0
            duplicates['recoverable_variance'] = duplicates['debit']
            duplicates['violation_type'] = 'Potential Duplicate Debit Payload'
            duplicates['rule_reference'] = 'CBN Operational Guideline - Reversal Mandate'
            return duplicates
        return pd.DataFrame()
