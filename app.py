import streamlit as st

# System Configuration
st.set_page_config(
    page_title="Executive Intelligence Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header Architecture
st.title("🛡️ Executive Intelligence Suite")
st.caption("Bamidele Adedeji & Associates | Forensic Analytics & Revenue Assurance Engine")

st.markdown("---")

# Modular Gateway Notice
st.info(" Core Engine Status: Online. Ready for modular rule integration.")

import streamlit as st
import pandas as pd
import io

from core.schema import UniversalAuditSchema
from core.forensic_rules import UniversalForensicEngine
from reports.ledgers import UniversalLedgerExporter

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & HEADER
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Executive Intelligence Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛡️ Universal Executive Intelligence Suite")
st.caption("Bamidele Adedeji & Associates | Forensic Analytics & Revenue Assurance Engine")
st.markdown("---")

# -----------------------------------------------------------------------------
# STEP 1: FILE INGESTION
# -----------------------------------------------------------------------------
st.subheader("Step 1: Upload Client Statement or POS Log")
uploaded_file = st.file_uploader(
    "Select client file (CSV or Excel format):",
    type=["csv", "xlsx", "xls"],
    help="Upload structured data to run automated Money, Operations, and Risk audits."
)

if uploaded_file is not None:
    try:
        # Load raw file
        if uploaded_file.name.endswith('.csv'):
            raw_df = pd.read_csv(uploaded_file)
        else:
            raw_df = pd.read_excel(uploaded_file)

        st.success(f"File uploaded successfully: **{uploaded_file.name}** ({len(raw_df):,} records)")

        # Validate Schema
        clean_df = UniversalAuditSchema.validate_and_clean(raw_df)

        # -----------------------------------------------------------------------------
        # STEP 2: TRIPLE-PILLAR FORENSIC EXECUTION
        # -----------------------------------------------------------------------------
        st.markdown("---")
        st.subheader("Step 2: Triple-Pillar Forensic Findings")

        # Execute Engine Rules
        money_findings = UniversalForensicEngine.audit_money_pillar(clean_df)
        ops_findings = UniversalForensicEngine.audit_operations_pillar(clean_df)
        risk_findings = UniversalForensicEngine.audit_risk_pillar(clean_df)

        # Combine Findings
        all_findings = pd.concat([money_findings, ops_findings, risk_findings], ignore_index=True)

        # -----------------------------------------------------------------------------
        # METRIC CARDS DISPLAY
        # -----------------------------------------------------------------------------
        col1, col2, col3, col4 = st.columns(4)
        
        gross_rec = money_findings['recoverable_variance'].sum() if not money_findings.empty else 0.0
        
        col1.metric("Total Records Reviewed", f"{len(clean_df):,}")
        col2.metric("Money Findings (Overcharges)", f"{len(money_findings):,}")
        col3.metric("Gross Recovery Target", f"₦{gross_rec:,.2f}")
        col4.metric("Audit Fee (15%)", f"₦{(gross_rec * 0.15):,.2f}")

        # Display Interactive Tabs
        tab_money, tab_ops, tab_risk = st.tabs(["💰 Money Pillar (Recoveries)", "⚙️ Operations Pillar (Latency)", "🛡️ Risk Pillar (Exposure)"])

        with tab_money:
            st.markdown("### Revenue Assurance & Recovery Findings")
            if not money_findings.empty:
                st.dataframe(money_findings, use_container_width=True)
            else:
                st.info("No fee overcharges or duplicate debits detected.")

        with tab_ops:
            st.markdown("### Operational Latency & Off-Hours Activity")
            if not ops_findings.empty:
                st.dataframe(ops_findings, use_container_width=True)
            else:
                st.info("All transactions fell within normal operating hours.")

        with tab_risk:
            st.markdown("### Statistical Outliers & Compliance Risks")
            if not risk_findings.empty:
                st.dataframe(risk_findings, use_container_width=True)
            else:
                st.info("No high-value outliers identified.")

        # -----------------------------------------------------------------------------
        # STEP 3: DOWNLOAD EXCEL REPORT
        # -----------------------------------------------------------------------------
        st.markdown("---")
        st.subheader("Step 3: Download Executive Forensic Report")

        buffer = io.BytesIO()
        UniversalLedgerExporter.generate_excel_report(clean_df, all_findings, buffer)

        st.download_button(
            label="📥 Download Official 5-Tab Forensic Report (.xlsx)",
            data=buffer.getvalue(),
            file_name=f"BAA_FORENSIC_REPORT_{pd.Timestamp.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )

    except Exception as e:
        st.error(f"Error processing file: {e}")
