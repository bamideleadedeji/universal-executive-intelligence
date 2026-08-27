import pandas as pd

class ExcelReportGenerator:
    """
    Generates professional 5-tab Forensic Excel Audit Reports.
    """
    @staticmethod
    def generate_report(master_df: pd.DataFrame, findings_df: pd.DataFrame, output_path: str):
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            
            # 1. Executive Summary Sheet
            total_rev = len(master_df)
            total_infractions = len(findings_df) if not findings_df.empty else 0
            gross_recovery = findings_df['recoverable_variance'].sum() if not findings_df.empty else 0.0
            
            exec_summary = pd.DataFrame([
                {"Forensic Indicator": "Total Transactions Reviewed", "Audit Value": total_rev},
                {"Forensic Indicator": "Systemic Regulatory Infractions Located", "Audit Value": total_infractions},
                {"Forensic Indicator": "Gross Recoverable Variance Target (NGN)", "Audit Value": gross_recovery},
                {"Forensic Indicator": "Client Recovery Share (85%)", "Audit Value": gross_recovery * 0.85},
                {"Forensic Indicator": "Audit Contingency Fee (15%)", "Audit Value": gross_recovery * 0.15}
            ])
            exec_summary.to_excel(writer, sheet_name='Executive Summary', index=False)
            
            # 2. Master Statement
            master_df.to_excel(writer, sheet_name='Master Statement', index=False)
            
            # 3. Complaint & Evidence Ledger
            if not findings_df.empty:
                findings_df.to_excel(writer, sheet_name='Complaint Ledger', index=False)
                findings_df[['source_row', 'transaction_date', 'narration', 'debit', 'allowed_fee', 'recoverable_variance', 'violation_type', 'rule_reference']].to_excel(writer, sheet_name='Evidence Register', index=False)
            else:
                pd.DataFrame([{"Status": "No infractions detected"}]).to_excel(writer, sheet_name='Complaint Ledger', index=False)
