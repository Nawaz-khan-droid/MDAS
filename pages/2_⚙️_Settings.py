import streamlit as st

st.set_page_config(page_title="MDAS | Settings", page_icon="⚙️", layout="wide")

st.title("⚙️ System Settings & Integrations")

st.markdown("### 🔌 Keyless API Integration")
st.write("MDAS exposes a modular FastAPI backend that allows programmatic access to the multi-dimensional analysis pipeline without requiring API keys.")

st.info("**Note for Streamlit Cloud Users:** Streamlit Cloud runs UI-only instances. To host this API, deploy the codebase to a platform like Render, Railway, or AWS, and run `uvicorn mdas.api.main:app`.")

st.markdown("""
#### Start the API Server (Local/Docker)
```bash
# From the project root, run the Uvicorn server:
uvicorn src.mdas.api.main:app --host 0.0.0.0 --port 8000
```
""")

st.markdown("""
#### Example Usage (cURL)
```bash
curl -X POST "http://localhost:8000/api/analyze" \\
     -H "Content-Type: application/json" \\
     -d '{"text": "URGENT: The database crashed, fix it now!"}'
```
""")

st.markdown("""
#### Example Usage (Python / Requests)
```python
import requests

response = requests.post(
    "http://localhost:8000/api/analyze",
    json={"text": "The new update looks great! Keep it up."}
)

data = response.json()
print("Sentiment:", data["radar"]["sentiment"])
print("Urgency:", data["radar"]["urgency"])
```
""")

st.divider()

st.markdown("### 🛠️ UI Preferences")
sidebar_state = st.radio("Default Sidebar State", ["Expanded", "Collapsed"], index=1)
st.caption("Settings persist across active session state.")
