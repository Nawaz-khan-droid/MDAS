import streamlit as st

st.set_page_config(page_title="MDAS | Docs", page_icon="📖", layout="wide")

st.title("📖 Documentation")
st.markdown("""
### Multi-Dimensional Text Analysis System (MDAS)

MDAS is an advanced, offline-first Natural Language Processing pipeline built for high-throughput operational intelligence. It operates as a **Modular Monolith**, ensuring zero external API latency, absolute data privacy, and immediate inference without cloud roundtrips.

#### Core Capabilities
- **Behavioral Risk Radar**: Scores incoming text on 5 axes (Sentiment, Urgency, Churn Risk, Toxicity, Sarcasm).
- **Classification Engine**: Fast, local `scikit-learn` models for Intent, Category Domain, and Spam detection.
- **Linguistic Extraction**: Uses `spaCy` to extract grammar, voice (Active/Passive), and Named Entities (NER).

#### System Architecture
MDAS is designed natively in Python, featuring:
1. **Streamlit UI**: The operational dashboard you are currently viewing.
2. **FastAPI Backend**: A keyless REST API available for downstream microservices.
3. **Core ML Package**: The `mdas` Python package powering the engine.

#### How to use the API
See the **⚙️ Settings** page for details on integrating the Keyless API.
""")
