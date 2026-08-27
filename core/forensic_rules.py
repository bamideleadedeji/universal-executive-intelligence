import pandas as pd
import numpy as np

class UniversalForensicEngine:
    """
    Unified Triple-Pillar Engine: Money, Operations, and Risk.
    Executes concurrent forensic audits across all three business pillars.
    """

    # -------------------------------------------------------------------------
    # PILLAR 1: MONEY ENGINE (Revenue Assurance & Overcharge Calculation)
    # -------------------------------------------------------------------------
   # 1. FIX OPERATIONS PILLAR: Require explicit timestamp before running off-hours check
@staticmethod
def audit_operations_pillar(df: pd.DataFrame) -> pd.DataFrame:
    df_ops = df.copy()
    # Only run off-hours check if real timestamps (non-midnight) are present
    has_time = df_ops['transaction_date'].dt.time.ne(pd.Timestamp("00:00:00").time()).any()
    if not has_time:
        return pd.DataFrame()  # Suppress false positives when only date is available
    
    # Run off-hours logic...

        # 1. SMS Notification Overcharges
        sms_mask = df_money['narration'].str.contains('SMS', case=False, na=False) & (df_money['debit'] > 0)
        for idx, row in df_money[sms_mask].iterrows():
            actual = row['debit']
            if actual > sms_cap:
                variance = actual - sms_cap
                findings.append({
                    'source_row': row['source_row'],
                    'transaction_date': row['transaction_date'],
                    'narration': row['narration'],
                    'pillar': 'MONEY',
                    'audit_category': 'Excess SMS Charge',
                    'actual_value': actual,
                    'allowed_value': sms_cap,
                    'recoverable_variance': variance,
                    'rule_reference': 'CBN Guide to Bank Charges (Sec 10.3)'
                })

        # 2. Duplicate Outflow Payload Check
        debits = df_money[df_money['debit'] > 0].copy()
        debits['date_only'] = debits['transaction_date'].dt.date
        dup_mask = debits.duplicated(subset=['date_only', 'debit', 'narration'], keep=False)
        
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
                'rule_reference': 'CBN Operational Guideline - Mandatory Reversal Rule'
            })

        return pd.DataFrame(findings)

    # -------------------------------------------------------------------------
    # PILLAR 2: OPERATIONS ENGINE (Latency, Off-Hours & Bottlenecks)
    # -------------------------------------------------------------------------
    @staticmethod
    def audit_operations_pillar(df: pd.DataFrame) -> pd.DataFrame:
        """Audits transaction timestamps, off-hours processing, and throughput."""
        df_ops = df.copy()
        findings = []

        # Flag Off-Hours Activity (10 PM to 6 AM)
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
                'recoverable_variance': 0.0,  # Operational finding, non-direct recoverable
                'rule_reference': 'Internal Control Standard - Operating Hours Window'
            })

        return pd.DataFrame(findings)

    # -------------------------------------------------------------------------
    # PILLAR 3: RISK ENGINE (Outliers, Structuring & Anomalies)
    # -------------------------------------------------------------------------
    @staticmethod
    def audit_risk_pillar(df: pd.DataFrame, percentile: float = 0.99) -> pd.DataFrame:
        """Isolates high-value statistical outliers and suspicious threshold activity."""
        df_risk = df.copy()
        findings = []

        debits = df_risk[df_risk['debit'] > 0]
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
