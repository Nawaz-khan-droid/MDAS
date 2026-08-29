import streamlit as st
import json
from pathlib import Path
from mdas.classification.registry import ModelRegistry

st.set_page_config(
    page_title="MDAS | Settings & Keyless API",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.sidebar.title("🧭 MDAS Controls")
st.sidebar.markdown("### 📚 Navigation")
st.sidebar.page_link("mdas_dashboard.py", label="Operational Radar", icon="🧭")
st.sidebar.page_link("pages/1_📖_Docs.py", label="Documentation & Specs", icon="📖")
st.sidebar.page_link("pages/2_⚙️_Settings.py", label="Keyless API & Settings", icon="⚙️")

st.title("⚙️ System Settings & Keyless API Integration")
st.caption("Configure operational thresholds and connect downstream microservices via Keyless REST API.")

set_tab1, set_tab2, set_tab3 = st.tabs([
    "🔌 Keyless REST API Guide", 
    "🤖 Model Registry Status", 
    "🎛️ Operational Thresholds"
])

with set_tab1:
    st.markdown("""
    ### 🔌 Keyless REST API Endpoint
    
    MDAS includes an embedded, high-performance **FastAPI** backend (`src/mdas/api/main.py`). 
    Because it runs entirely offline within your infrastructure, **no API keys, billing tokens, or external auth** are required.
    
    #### How to Launch the API Server:
    ```bash
    # Run the Uvicorn ASGI server from project root:
    uvicorn src.mdas.api.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    
    #### Live REST Endpoints:
    - **`GET /health`**: Returns system health and loaded model status.
    - **`POST /api/analyze`**: Performs multi-dimensional text analysis and returns the complete JSON contract.
    """)

    st.markdown("#### cURL Integration Example:")
    st.code("""curl -X POST "http://localhost:8000/api/analyze" \\
     -H "Content-Type: application/json" \\
     -d '{"text": "URGENT: Our production database is down!"}'""", language="bash")

    st.markdown("#### Python Requests Client Example:")
    st.code("""import requests

url = "http://localhost:8000/api/analyze"
payload = {"text": "URGENT: Broken payment gateway!"}

response = requests.post(url, json=payload)
data = response.json()

print("Urgency Score: ", data["radar"]["urgency"])
print("Churn Risk:    ", data["radar"]["churn_risk"])
print("Classification:", data["classification"]["intent"]["label"])""", language="python")

with set_tab2:
    st.markdown("### 🤖 Loaded Model Registry Inspector")
    registry = ModelRegistry(Path("models"))
    loaded_tasks = registry.list_tasks()
    
    st.write(f"**Total Loaded Models:** `{len(loaded_tasks)}`")
    
    for task in loaded_tasks:
        with st.expander(f"Model: {task.upper()}", expanded=True):
            meta_file = Path("models") / f"{task}.json"
            if meta_file.exists():
                meta_content = json.loads(meta_file.read_text(encoding="utf-8"))
                c1, c2, c3 = st.columns(3)
                c1.write(f"**Algorithm:** `{meta_content.get('model_type', 'LinearSVC')}`")
                c2.write(f"**Classes:** `{len(meta_content.get('classes', []))}` classes")
                c3.write(f"**Domain:** `{meta_content.get('domain', 'general')}`")
                st.json(meta_content)
            else:
                st.info(f"Binary model `{task}.joblib` loaded without metadata sidecar.")

with set_tab3:
    st.markdown("### 🎛️ Operational Alert Thresholds")
    st.slider("Critical Urgency Threshold", min_value=0.5, max_value=1.0, value=0.67, step=0.01)
    st.slider("Critical Churn Risk Threshold", min_value=0.5, max_value=1.0, value=0.85, step=0.01)
    st.slider("Toxicity Moderation Alert Threshold", min_value=0.3, max_value=0.8, value=0.50, step=0.01)
    st.caption("Thresholds configure the operational dispatch rules for live support queue escalation.")
