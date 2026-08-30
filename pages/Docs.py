import streamlit as st

st.set_page_config(
    page_title="MDAS | Documentation",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("MDAS System Documentation & Specifications")
st.caption("Multi-Dimensional Text Analysis System • Architectural Reference Manual")

doc_tab1, doc_tab2, doc_tab3, doc_tab4 = st.tabs([
    "Architecture & Philosophy", 
    "5-Axis Radar Standards", 
    "Machine Learning Models", 
    "Linguistics & Voice Engine"
])

with doc_tab1:
    st.markdown("""
    ### 1. Architectural Philosophy: The Modular Monolith
    
    **MDAS** is designed as a self-contained, offline-first Natural Language Processing system. 
    
    #### Why a Modular Monolith?
    - **Zero Network Latency**: No third-party LLM API calls, no roundtrip network hops. Inferences execute locally in **< 3 milliseconds**.
    - **Total Data Privacy**: Sensitive customer communications, support tickets, and enterprise queries never leave your compute boundary.
    - **Low Cloud Costs**: Runs seamlessly on CPU-only free tier instances without requiring expensive GPUs or token billing.
    - **Deterministic Outputs**: Structured contracts and calibrated classifiers ensure zero hallucination in operational triage.
    
    ```
    ┌──────────────────────────────────────────────────────────────┐
    │                      MDAS Application                        │
    ├──────────────────────────────┬───────────────────────────────┤
    │      Streamlit Frontend      │      FastAPI REST Server      │
    │  (Operational Radar + Code)  │    (Keyless Microservice)     │
    ├──────────────────────────────┴───────────────────────────────┤
    │                      MDASAnalyzer Core                       │
    ├──────────────────────────────┬───────────────────────────────┤
    │        spaCy Backend         │     ModelRegistry (Sklearn)   │
    │  (Tokens, Voice, Entities)   │   (Intent, Category, Spam)    │
    └──────────────────────────────┴───────────────────────────────┘
    ```
    """)

with doc_tab2:
    st.markdown("""
    ### 2. The 5-Axis Operational Radar Standard
    
    Every incoming text is mapped to a standardized operational risk continuum from `0.0` (Baseline Calm) to `1.0` (Critical Emergency):
    
    | Axis | Metric Target | Visual 0.0 Mapping | Visual 1.0 Mapping |
    | :--- | :--- | :--- | :--- |
    | **Sentiment** | `sentiment` | Highly Positive (Green baseline) | Very Negative (Deep Red Flare) |
    | **Urgency** | `urgency` | Normal Priority Inquiry | Immediate Outage / Deadline (Flash Red) |
    | **Churn Risk** | `churn_risk` | Satisfied Customer | Immediate Cancellation / Competitor Threat |
    | **Toxicity** | `toxicity` | Professional Tone | Abusive Language / Harassment Flag |
    | **Sarcasm** | `sarcasm` | Literal Communication | Sarcastic Dissatisfaction / Mockery |
    
    #### Automated Dispatch Thresholds
    - **Urgency $\\ge 0.67$ and Churn $\\ge 0.70$**: Triggers **Critical Dispatch** to Senior Engineering SRE & Retention Taskforce.
    - **Urgency $\\ge 0.67$**: Triggers **Critical Dispatch** to On-Call SRE Incident Response.
    - **Churn Risk $\\ge 0.70$**: Triggers **Retention Review** for Customer Success intervention.
    - **Toxicity $\\ge 0.50$**: Triggers **Content Moderation Review** for employee well-being.
    - **Urgency $\\ge 0.34$**: Routes to **Tier-2 Specialized Support**.
    - **Otherwise**: Enters **Routine Automated Processing**.
    """)

with doc_tab3:
    st.markdown("""
    ### 3. Machine Learning Models & Inference
    
    MDAS bundles 4 scikit-learn models serialized with `joblib`, running high-speed n-gram TF-IDF vectorization:
    
    1. **Intent Classifier (`models/intent.joblib`)**:
       - Multi-class classifier distinguishing between `inquiry`, `complaint`, `cancellation`, `feedback`, `support_request`, and `billing`.
    2. **Category Domain Classifier (`models/category.joblib`)**:
       - Categorizes incoming tickets into domain verticals (`technical`, `billing`, `account`, `product`, `general`).
    3. **Spam & Security Filter (`models/spam.joblib`)**:
       - High-precision binary classifier isolating phishing, spam giveaways, and malicious payloads from authentic customer inquiries.
    4. **Sentiment Polarity (`models/sentiment.joblib`)**:
       - Calibrated 3-class sentiment classifier (`positive`, `neutral`, `negative`).
    """)

with doc_tab4:
    st.markdown("""
    ### 4. Deep Linguistics, Syntax & Voice Engine
    
    Powered by `spaCy`, MDAS performs comprehensive grammatical parse-tree inspection:
    
    - **Grammatical Voice Detection**: Distinguishes **Active**, **Active (Imperative)**, and **Passive** voice based on auxiliary verbs (`aux:pass`, `auxpass`, BE+VBN participles), passive subjects (`nsubj:pass`), and imperative mood roots.
    - **Named Entity Recognition (NER)**: Extracts organizations (`ORG`), monetary amounts (`MONEY`), dates (`DATE`), locations (`GPE`), people (`PERSON`), URLs, and identifiers (`ORDER_ID`, `TRANSACTION_ID`).
    - **Lexical Complexity**: Computes Type-Token Ratio (TTR) lexical diversity, average words per sentence, and root lemma distributions.
    """)
