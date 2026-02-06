
# Contract Risk & Compliance Assistant
### Run 
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py

# Features
Understands what type of contract it is
Breaks the contract into readable clauses So users can review section-by-section instead of reading a huge legal document.
Analyzes each clause for potential risks The system looks for legally sensitive wording and flags risky terms.
Assigns a clear risk score to every clause Each section is marked as Low, Medium, or High risk.
Generates an overall contract risk score which gives business owners a quick snapshot of how risky the agreement is.
Identifies critical clauses that need attention such as termination without notice, liability exclusions, non-compete clauses, and penalties.
Uses a dynamic risk escalation model and Multiple high-risk clauses increase the overall exposure intelligently.
Generates a downloadable PDF report which is ready to share with legal advisors or management.
Detects contract language (English or Hindi) and processes it appropriately for analysis.
Maintains an audit log
