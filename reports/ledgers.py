import pandas as pd

class UniversalLedgerExporter:
    """
    Generates a professional 5-Tab Forensic Excel Report covering Money, Operations, and Risk.
    """
    @staticmethod
    def generate_excel_report(master_df: pd.DataFrame, findings_df: pd.DataFrame, output_path: str):
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            
            # 1. Executive Summary Sheet
            total_records = len(master_df)
            total_findings = len(findings_df) if not findings_df.empty else 0
            
            recoverable_target = 0.0
            if not findings_df.empty and 'recoverable_variance' in findings_df.columns:
                recoverable_target = findings_df['recoverable_variance'].sum()

            exec_summary = pd.DataFrame([
                {"Forensic Indicator": "Total Transactions Reviewed", "Audit Value": total_records},
                {"Forensic Indicator": "Total Pillar Infractions / Flags Identified", "Audit Value": total_findings},
                {"Forensic Indicator": "Gross Recoverable Variance Target (NGN)", "Audit Value": recoverable_target},
                {"Forensic Indicator": "Client Net Recovery Share (85%)", "Audit Value": recoverable_target * 0.85},
                {"Forensic Indicator": "Audit Contingency Fee (15%)", "Audit Value": recoverable_target * 0.15}
            ])
            exec_summary.to_excel(writer, sheet_name='Executive Summary', index=False)
            
            # 2. Master Normalized Statement
            master_df.to_excel(writer, sheet_name='Master Statement', index=False)
            
            # 3. Triple-Pillar Complaint Ledger
            if not findings_df.empty:
                findings_df.to_excel(writer, sheet_name='Complaint Ledger', index=False)
                
                # 4. Evidence Register (Source Row Mapping)
                evidence_cols = [c for c in ['source_row', 'transaction_date', 'narration', 'pillar', 'audit_category', 'actual_value', 'recoverable_variance', 'rule_reference'] if c in findings_df.columns]
                findings_df[evidence_cols].to_excel(writer, sheet_name='Evidence Register', index=False)
                
                # 5. Pillar-Specific Risk Ledger
                risk_df = findings_df[findings_df['pillar'] == 'RISK']
                if not risk_df.empty:
                    risk_df.to_excel(writer, sheet_name='Risk Dashboard', index=False)
                else:
                    pd.DataFrame([{"Status": "No high-risk anomalies identified"}]).to_excel(writer, sheet_name='Risk Dashboard', index=False)
            else:
                pd.DataFrame([{"Status": "No infractions detected across Money, Operations, or Risk"}]).to_excel(writer, sheet_name='Complaint Ledger', index=False)
