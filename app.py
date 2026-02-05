import streamlit as st
import tempfile
from utils import extract_text_from_file, detect_language, normalize_text
from nlp_engine import process_contract, classify_contract_type
from risk_engine import compute_contract_risk
from pdf_report import generate_pdf_report
from audit import save_audit_log

st.set_page_config(
    page_title="Contract Risk Assistant",
    page_icon="",
    layout="wide"
)

# -------------------------
# Custom CSS Styling
# -------------------------
st.markdown("""
<style>
.big-font {
    font-size:28px !important;
    font-weight:600;
}
.risk-high { color: #ff4b4b; font-weight:600; }
.risk-medium { color: #ffa500; font-weight:600; }
.risk-low { color: #2ecc71; font-weight:600; }
.card {
    padding:20px;
    border-radius:12px;
    background-color:#111827;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.markdown("<div class='big-font'>🏛 AI Contract and Risk Assessment Bot</div>", unsafe_allow_html=True)
st.caption("GenAI-powered Legal Intelligence for Indian SMEs")
st.divider()

# -------------------------
# Upload Section
# -------------------------
uploaded_file = st.file_uploader(
    "Upload Contract (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        file_path = tmp.name

    raw_text = extract_text_from_file(file_path, uploaded_file.type)
    language = detect_language(raw_text)
    text = normalize_text(raw_text)

    contract_type = classify_contract_type(text)

    st.success(f"Detected Contract Type: {contract_type}")
    st.info(f"Detected Language: {language}")

    st.divider()

    if st.button("🚀 Run Full Risk Analysis", use_container_width=True):

        with st.spinner("Analyzing contract..."):

            nlp_results = process_contract(text)
            risk_results = compute_contract_risk(nlp_results["clauses"])

            save_audit_log({
                "contract_type": contract_type,
                "language": language,
                "risk_score": risk_results["composite_score"]
            })

            score = risk_results["composite_score"]

            # Risk Level Label
            if score >= 8:
                level = "High Risk"
                level_class = "risk-high"
            elif score >= 5:
                level = "Moderate Risk"
                level_class = "risk-medium"
            else:
                level = "Low Risk"
                level_class = "risk-low"

            # -------------------------
            # Dashboard Section
            # -------------------------
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Composite Risk Score", score)

            with col2:
                st.markdown(f"<h3 class='{level_class}'>{level}</h3>", unsafe_allow_html=True)

            st.progress(score / 10)

            st.divider()

            # -------------------------
            # High Risk Clauses
            # -------------------------
            st.subheader("🚩 High Risk Clauses")

            if risk_results["high_risk_clauses"]:
                for clause in risk_results["high_risk_clauses"]:
                    st.error(clause[:200] + "...")
            else:
                st.success("No high-risk clauses detected.")

            st.divider()

            # -------------------------
            # Clause Breakdown
            # -------------------------
            st.subheader("📌 Clause-Level Breakdown")

            for clause in risk_results["clause_risks"]:
                with st.expander(f"{clause['risk']} Risk Clause"):
                    st.write(clause["text"])

            st.divider()

            # -------------------------
            # Executive Summary
            # -------------------------
            st.subheader("📝 Executive Summary")
            st.write(risk_results["summary"])

            st.divider()

            # -------------------------
            # Download Report
            # -------------------------
            pdf_path = generate_pdf_report(contract_type, risk_results)

            with open(pdf_path, "rb") as f:
                st.download_button(
                    "📥 Download Legal Review Report (PDF)",
                    f,
                    file_name="contract_risk_report.pdf",
                    use_container_width=True
                )

            st.success("Analysis Complete.")
