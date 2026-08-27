import pandas as pd

class UniversalForensicEngine:
    """
    Unified Triple-Pillar Engine: Money, Operations, and Risk.
    """

    @staticmethod
    def audit_money_pillar(df: pd.DataFrame, sms_cap: float = 4.00) -> pd.DataFrame:
        """Audits fee overcharges, SMS rates, and duplicate debit payloads."""
        findings = []

        # 1. SMS Notification Overcharges (CBN N4 Cap)
        sms_mask = df['narration'].str.contains('SMS', case=False, na=False) & (df['debit'] > 0)
        for idx, row in df[sms_mask].iterrows():
            actual = row['debit']
            if actual > sms_cap:
                findings.append({
                    'source_row': row['source_row'],
                    'transaction_date': row['transaction_date'],
                    'narration': row['narration'],
                    'pillar': 'MONEY',
                    'audit_category': 'Excess SMS Charge',
                    'actual_value': actual,
                    'allowed_value': sms_cap,
                    'recoverable_variance': actual - sms_cap,
                    'rule_reference': 'CBN Guide to Bank Charges (Sec 10.3)'
                })

        # 2. Duplicate Outflow Payload Check
        debits = df[df['debit'] > 0].copy()
        debits['tx_date_only'] = debits['transaction_date'].dt.date
        dup_mask = debits.duplicated(subset=['tx_date_only', 'debit', 'narration'], keep=False)
        
        for idx, row in debits[dup_mask].iterrows():
            findings.append({
                'source_row': row['source_row'],
                'transaction_date': row['transaction_date'],
                'narration': row['narration'],
                'pillar': 'MONEY',
                'audit_category': 'Potential Duplicate Debit Payload',
                'actual_value': row['debit'],
                'allowed_value': 0.0,
                'recoverable_variance': row['debit'],
                'rule_reference': 'CBN Operational Guideline - Reversal Mandate'
            })

        return pd.DataFrame(findings)

    @staticmethod
    def audit_operations_pillar(df: pd.DataFrame) -> pd.DataFrame:
        """Audits processing latency and off-hours activity (Suppresses false positives on date-only files)."""
        findings = []

        # Only run off-hours check if real timestamps (non-midnight 00:00:00) exist
        has_time_data = df['transaction_date'].dt.time.ne(pd.Timestamp("00:00:00").time()).any()
        if not has_time_data:
            return pd.DataFrame()

        df_ops = df.copy()
        df_ops['hour'] = df_ops['transaction_date'].dt.hour
        off_hours_mask = (df_ops['hour'] < 6) | (df_ops['hour'] >= 22)

        for idx, row in df_ops[off_hours_mask].iterrows():
            val = row['debit'] if row['debit'] > 0 else row['credit']
            findings.append({
                'source_row': row['source_row'],
                'transaction_date': row['transaction_date'],
                'narration': row['narration'],
                'pillar': 'OPERATIONS',
                'audit_category': 'Off-Hours Ledger Activity',
                'actual_value': val,
                'allowed_value': 0.0,
                'recoverable_variance': 0.0,
                'rule_reference': 'Internal Control Standard - Operating Hours Window'
            })

        return pd.DataFrame(findings)

    @staticmethod
    def audit_risk_pillar(df: pd.DataFrame, percentile: float = 0.99) -> pd.DataFrame:
        """Isolates high-value statistical outliers."""
        findings = []
        debits = df[df['debit'] > 0]
        
        if not debits.empty:
            q_threshold = debits['debit'].quantile(percentile)
            outliers = debits[debits['debit'] >= q_threshold]

            for idx, row in outliers.iterrows():
                findings.append({
                    'source_row': row['source_row'],
                    'transaction_date': row['transaction_date'],
                    'narration': row['narration'],
                    'pillar': 'RISK',
                    'audit_category': 'High-Value Outlier Exposure',
                    'actual_value': row['debit'],
                    'allowed_value': q_threshold,
                    'recoverable_variance': 0.0,
                    'rule_reference': f'AML/CFT Risk Threshold Audit (Top {int((1-percentile)*100)}%)'
                })

        return pd.DataFrame(findings)
