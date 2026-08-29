import streamlit as st
import plotly.graph_objects as go
import time
import json
from pathlib import Path
from mdas import MDASAnalyzer

# --- Page Configuration ---
st.set_page_config(
    page_title="MDAS | Multi-Dimensional Text Analysis",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Theme-Adaptive CSS & Material-Mesop Styling ---
st.markdown("""
<style>
    /* Top Bar */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(128, 128, 128, 0.2);
        padding-bottom: 8px;
        margin-bottom: 16px;
    }
    .pane-title {
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        color: var(--text-color);
        opacity: 0.8;
    }
    .status-badge {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.78rem;
    }
    
    /* Symmetric Metric Card */
    .kpi-card {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.18);
        border-radius: 8px;
        padding: 12px 10px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .kpi-title {
        font-size: 0.72rem;
        text-transform: uppercase;
        font-weight: 600;
        opacity: 0.65;
        margin-bottom: 4px;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-color);
    }

    /* Action Alerts */
    .action-box {
        padding: 14px 16px;
        border-radius: 8px;
        margin-top: 14px;
        margin-bottom: 14px;
        font-weight: 500;
        display: flex;
        align-items: flex-start;
        gap: 12px;
        font-size: 0.92rem;
    }
    .action-critical {
        background-color: rgba(239, 68, 68, 0.12);
        border-left: 4px solid #ef4444;
        color: #ef4444;
    }
    .action-warning {
        background-color: rgba(245, 158, 11, 0.12);
        border-left: 4px solid #f59e0b;
        color: #f59e0b;
    }
    .action-routine {
        background-color: rgba(59, 130, 246, 0.12);
        border-left: 4px solid #3b82f6;
        color: #3b82f6;
    }

    /* Tag Pills */
    .tag-chip {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        background-color: rgba(128, 128, 128, 0.12);
        border: 1px solid rgba(128, 128, 128, 0.2);
        margin: 2px 4px 2px 0;
    }
    
    /* Code Pane styling */
    .code-container {
        border-left: 1px solid rgba(128, 128, 128, 0.15);
        padding-left: 16px;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Global MDAS Engine ---
@st.cache_resource(show_spinner="Initializing MDAS NLP Engine & Model Registry...")
def get_analyzer():
    return MDASAnalyzer.from_directory("models")

try:
    analyzer = get_analyzer()
    engine_ready = True
except Exception as e:
    engine_ready = False
    init_error = str(e)

if not engine_ready:
    st.error(f"Failed to load MDAS Engine: {init_error}")
    st.stop()

# --- Sample Library ---
SAMPLE_QUERIES = {
    "🚨 Urgent Outage": "URGENT: Production payment gateway is down and throwing 500 errors. Fix this immediately or I am canceling our enterprise agreement today!",
    "🚪 Churn Risk": "I am deeply disappointed with the latest software update. The UI is clunky and slow. We are seriously evaluating switching to your competitor next month.",
    "💬 Billing Inquiry": "Hello support team, could you please explain why our invoice #84920 includes a 15% recurring cloud surcharge? Thank you.",
    "🎭 Sarcastic Ticket": "Oh brilliant engineering work, team. Deploying breaking database migrations on Friday evening without testing is truly a masterclass in QA.",
    "🛡️ Phishing Spam": "CONGRATULATIONS WINNER! You have won an exclusive $5,000 Apple Gift Card. Click here now to verify your credentials before this prize expires!",
    "🌟 Rave Review": "I am absolutely thrilled with this tool! The latency is lightning fast and our entire engineering workflow has doubled in productivity."
}

# --- Sidebar Controls ---
st.sidebar.title("🧭 MDAS Controls")
show_code_pane = st.sidebar.checkbox("Show Code / Developer Palette", value=True)
split_ratio = st.sidebar.radio("View Split Mode", ["50 / 50 Split", "60 / 40 Split", "Preview Only"], index=0)

st.sidebar.divider()
st.sidebar.markdown("### 📚 Navigation")
st.sidebar.page_link("mdas_dashboard.py", label="Operational Radar", icon="🧭")
st.sidebar.page_link("pages/1_📖_Docs.py", label="Documentation & Specs", icon="📖")
st.sidebar.page_link("pages/2_⚙️_Settings.py", label="Keyless API & Settings", icon="⚙️")

# --- Top Navigation Bar ---
top_left, top_right = st.columns([1.1, 1] if show_code_pane and split_ratio != "Preview Only" else [1, 0.001])
with top_left:
    st.markdown("""
    <div class="top-bar">
        <div class="pane-title">🖥️ Interactive Preview</div>
        <div class="status-badge">● Engine Online (v0.1.0)</div>
    </div>
    """, unsafe_allow_html=True)

if show_code_pane and split_ratio != "Preview Only":
    with top_right:
        st.markdown("""
        <div class="top-bar">
            <div class="pane-title">📄 Code & Integration Palette</div>
            <div style="font-size: 0.8rem; opacity: 0.6;">Python • REST • Architecture</div>
        </div>
        """, unsafe_allow_html=True)

# --- Layout Grid ---
if show_code_pane and split_ratio == "50 / 50 Split":
    col_preview, col_code = st.columns([1, 1])
elif show_code_pane and split_ratio == "60 / 40 Split":
    col_preview, col_code = st.columns([1.3, 1])
else:
    col_preview = st.container()
    col_code = None

# ==========================================
# LEFT PANE: PREVIEW & INTERACTION
# ==========================================
with col_preview:
    st.markdown("### 🧭 MDAS Operational Radar")
    st.caption("Multi-Dimensional Text Analysis System • Modular Monolith V0.1 • Fast Offline NLP")

    # Quick Samples Grid
    st.markdown("**Quick Example Prompts:**")
    sample_cols = st.columns(3)
    sample_items = list(SAMPLE_QUERIES.items())
    for idx, (s_name, s_text) in enumerate(sample_items):
        target_col = sample_cols[idx % 3]
        if target_col.button(s_name, key=f"samp_btn_{idx}", use_container_width=True):
            st.session_state["active_prompt"] = s_text

    current_prompt = st.session_state.get(
        "active_prompt", 
        "URGENT: Production payment gateway is down and throwing 500 errors. Fix this immediately or I am canceling our enterprise agreement today!"
    )

    # Input Box
    input_text = st.text_area(
        "Communication payload to analyze:",
        value=current_prompt,
        height=100,
        placeholder="Type or paste any customer communication, support ticket, review, or email..."
    )

    run_btn = st.button("⚡ Run Multi-Dimensional Analysis", type="primary", use_container_width=True)

    if input_text.strip():
        # Execute Engine
        t_start = time.perf_counter()
        analysis_obj = analyzer.analyze(input_text)
        latency_ms = (time.perf_counter() - t_start) * 1000
        res_dict = analysis_obj.to_dict()

        radar = res_dict.get("radar", {})
        signals = res_dict.get("signals", {})
        classification = res_dict.get("classification", {})
        stats = res_dict.get("statistics", {})
        ling = res_dict.get("linguistics", {})

        sentiment_label = (classification.get("sentiment", {}).get("label") or "Neutral").capitalize()
        intent_label = (classification.get("intent", {}).get("label") or "General").capitalize()
        cat_label = (classification.get("category", {}).get("label") or "Support").capitalize()
        spam_label = (classification.get("spam", {}).get("label") or "Ham").capitalize()

        urgency_score = radar.get("urgency", 0.0)
        churn_score = radar.get("churn_risk", 0.0)
        toxicity_score = radar.get("toxicity", 0.0)
        sarcasm_score = radar.get("sarcasm", 0.0)
        sentiment_score = radar.get("sentiment", 0.5)

        st.write("")

        # 5 Symmetric Top KPI Cards
        kpi_cols = st.columns(5)
        with kpi_cols[0]:
            sent_icon = "🟢" if sentiment_label == "Positive" else "🔴" if sentiment_label == "Negative" else "⚪"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Sentiment</div>
                <div class="kpi-value">{sent_icon} {sentiment_label}</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi_cols[1]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Primary Intent</div>
                <div class="kpi-value">🎯 {intent_label}</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi_cols[2]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Category Domain</div>
                <div class="kpi-value">📂 {cat_label}</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi_cols[3]:
            is_spam = spam_label.lower() == "spam"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Security Filter</div>
                <div class="kpi-value">{'🚨 Spam' if is_spam else '✅ Authentic'}</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi_cols[4]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Inference Time</div>
                <div class="kpi-value">⚡ {latency_ms:.2f} ms</div>
            </div>
            """, unsafe_allow_html=True)

        # Operational Action Dispatch Banner
        if urgency_score >= 0.67 or churn_score >= 0.85:
            st.markdown(f"""
            <div class="action-box action-critical">
                <span style="font-size: 1.4rem;">🚨</span>
                <div>
                    <strong>CRITICAL DISPATCH: Priority Live Queue</strong><br/>
                    High operational risk detected (Urgency: {urgency_score:.2f}, Churn Risk: {churn_score:.2f}). Escalated to Senior SRE & Account Retention playbook.
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif toxicity_score >= 0.50:
            st.markdown(f"""
            <div class="action-box action-warning">
                <span style="font-size: 1.4rem;">⚠️</span>
                <div>
                    <strong>CONTENT MODERATION: Staff Well-Being Review</strong><br/>
                    Elevated toxicity score ({toxicity_score:.2f}). Flagged for policy compliance and employee protection.
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif urgency_score >= 0.34 or churn_score >= 0.34:
            st.markdown(f"""
            <div class="action-box action-warning">
                <span style="font-size: 1.4rem;">🔔</span>
                <div>
                    <strong>TIER-2 ROUTING: Specialized {cat_label} Queue</strong><br/>
                    Moderate priority communication. Assigned to domain specialists for expedited response.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="action-box action-routine">
                <span style="font-size: 1.4rem;">ℹ️</span>
                <div>
                    <strong>ROUTINE TRIAGE: Standard Automation</strong><br/>
                    Low-risk communication. Queued for standard automated workflow processing.
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Radar & Signals
        r_col1, r_col2 = st.columns([1.1, 1])
        with r_col1:
            st.markdown("##### 🧭 5-Axis Operational Radar")
            radar_cats = ['Sentiment (Neg)', 'Urgency', 'Churn Risk', 'Toxicity', 'Sarcasm']
            radar_vals = [sentiment_score, urgency_score, churn_score, toxicity_score, sarcasm_score]

            fig = go.Figure()
            is_high_risk = urgency_score > 0.6 or churn_score > 0.6 or toxicity_score > 0.5
            fig.add_trace(go.Scatterpolar(
                r=radar_vals + [radar_vals[0]],
                theta=radar_cats + [radar_cats[0]],
                fill='toself',
                fillcolor='rgba(239, 68, 68, 0.22)' if is_high_risk else 'rgba(59, 130, 246, 0.22)',
                line=dict(
                    color='#ef4444' if is_high_risk else '#3b82f6',
                    width=2.5
                ),
                name='Operational Footprint'
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1],
                        showticklabels=True,
                        ticks='',
                        gridcolor='rgba(128, 128, 128, 0.2)'
                    ),
                    angularaxis=dict(
                        gridcolor='rgba(128, 128, 128, 0.2)',
                        tickfont=dict(size=11)
                    ),
                    bgcolor='rgba(0,0,0,0)'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(l=35, r=35, t=25, b=25),
                height=290
            )
            st.plotly_chart(fig, use_container_width=True)

        with r_col2:
            st.markdown("##### 🎯 Behavioral Risk Signals")
            def show_signal(title, val, label, ev_count, icon):
                color = "#10b981" if val < 0.34 else "#f59e0b" if val < 0.67 else "#ef4444"
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px;">
                    <span><strong>{icon} {title}</strong></span>
                    <span style="color: {color}; font-weight: 700; font-size: 0.85rem;">{label.upper()} ({val:.2f})</span>
                </div>
                """, unsafe_allow_html=True)
                st.progress(float(val))
                if ev_count:
                    st.caption(f"Trigger evidence count: {ev_count}")

            show_signal("Urgency", urgency_score, signals.get("urgency", {}).get("label", "low"), signals.get("urgency", {}).get("evidence_count", 0), "⚡")
            show_signal("Churn Risk", churn_score, signals.get("churn_risk", {}).get("label", "low"), signals.get("churn_risk", {}).get("evidence_count", 0), "🚪")
            show_signal("Toxicity", toxicity_score, signals.get("toxicity", {}).get("label", "low"), signals.get("toxicity", {}).get("evidence_count", 0), "☣️")
            show_signal("Sarcasm", sarcasm_score, signals.get("sarcasm", {}).get("label", "low"), signals.get("sarcasm", {}).get("marker_count", 0), "🎭")

        # Linguistic & Voice Breakdown
        with st.expander("🔍 Deep Linguistic Analysis & Grammatical Voice", expanded=False):
            ling_c1, ling_c2 = st.columns(2)
            with ling_c1:
                st.markdown("**🗣️ Active vs. Passive Voice:**")
                voice_summary = ling.get("voice", {}).get("summary", {})
                st.write(f"- Active Sentences: `{voice_summary.get('active', 0)}`")
                st.write(f"- Passive Sentences: `{voice_summary.get('passive', 0)}`")
                st.write(f"- Uncertain Sentences: `{voice_summary.get('uncertain', 0)}`")
                
                sentences = ling.get("voice", {}).get("sentences", [])
                for s in sentences:
                    st.markdown(f"- *\"{s.get('text')}\"* → **{s.get('voice')} Voice**")

            with ling_c2:
                st.markdown("**🏷️ Extracted Named Entities:**")
                entities = ling.get("entities", [])
                if entities:
                    chips = "".join([f"<span class='tag-chip'>🏷️ {e.get('text')} ({e.get('label')})</span>" for e in entities])
                    st.markdown(chips, unsafe_allow_html=True)
                else:
                    st.info("No named entities detected.")

                st.markdown("**📊 Text Complexity:**")
                st.write(f"- Words: `{stats.get('words', 0)}` | Sentences: `{stats.get('sentences', 0)}`")
                st.write(f"- Lexical Diversity (TTR): `{stats.get('lexical_diversity', 0):.2f}`")

    else:
        st.info("💡 Enter text above or choose a quick prompt to trigger the multi-dimensional analysis.")
        res_dict = None
        input_text = ""

# ==========================================
# RIGHT PANE: CODE & INTEGRATION PALETTE
# ==========================================
if col_code:
    with col_code:
        st.markdown("### 📄 Code & Integration Palette")
        st.caption("Interactive developer view replicating the Mesop code workspace.")

        code_tab1, code_tab2, code_tab3, code_tab4 = st.tabs([
            "🐍 Python Client", 
            "🌐 Keyless REST API", 
            "⚡ App Pipeline Code", 
            "📋 Output JSON"
        ])

        # 1. Python SDK
        with code_tab1:
            escaped_prompt = input_text.replace('"', '\\"').replace('\n', ' ') if input_text else "URGENT: Broken payment system!"
            python_sdk_code = f'''# --- MDAS Python SDK Client ---
# Install: pip install -e .
from mdas import MDASAnalyzer

# 1. Load the Offline Modular Monolith Engine
analyzer = MDASAnalyzer.from_directory("models")

# 2. Execute Multi-Dimensional Analysis
text = "{escaped_prompt}"
result = analyzer.analyze(text)

# 3. Access 5-Axis Radar Signals & Classifications
data = result.to_dict()
print("Sentiment Polarity:", data["radar"]["sentiment"])
print("Urgency Score:     ", data["radar"]["urgency"])
print("Churn Risk:        ", data["radar"]["churn_risk"])
print("Primary Intent:    ", data["classification"]["intent"]["label"])
print("Grammatical Voice: ", data["linguistics"]["voice"]["summary"])
'''
            st.code(python_sdk_code, language="python", line_numbers=True)

        # 2. Keyless REST API
        with code_tab2:
            escaped_prompt = input_text.replace('"', '\\"').replace('\n', ' ') if input_text else "URGENT: Broken payment system!"
            rest_code = f'''# ==========================================
# 1. cURL Terminal Request (Keyless API)
# ==========================================
curl -X POST "http://localhost:8000/api/analyze" \\
     -H "Content-Type: application/json" \\
     -d '{{"text": "{escaped_prompt}"}}'

# ==========================================
# 2. Python Requests Client
# ==========================================
import requests

response = requests.post(
    "http://localhost:8000/api/analyze",
    json={{"text": "{escaped_prompt}"}}
)

payload = response.json()
print("Urgency Score:", payload["radar"]["urgency"])
print("Action Route: ", payload["classification"]["category"]["label"])
'''
            st.code(rest_code, language="python", line_numbers=True)

        # 3. App Pipeline Code
        with code_tab3:
            pipeline_code = '''# --- MDAS Core Modular Pipeline Architecture ---
from dataclasses import dataclass
from mdas.nlp.spacy_backend import SpacyBackend
from mdas.classification.registry import ModelRegistry
from mdas.analysis.signals import build_signals
from mdas.analysis.voice import analyze_voice

class MDASAnalyzer:
    """Core monolithic analysis service."""
    def __init__(self, backend, registry=None, config=None):
        self.backend = backend
        self.registry = registry
        self.config = config

    def analyze(self, text: str):
        # 1. Tokenize and extract linguistic parse tree
        doc = self.backend.analyze(text)
        
        # 2. Extract syntactic voice & statistics
        voice = analyze_voice(doc)
        
        # 3. Model Registry multi-task inference
        classification = {}
        for task in ("sentiment", "intent", "category", "spam"):
            classification[task] = self.registry.predict(task, text)
            
        # 4. Synthesize 5-Axis Operational Radar
        signals = build_signals(text, classification["sentiment"].label)
        radar = {
            "sentiment": signals["sentiment"]["score"],
            "urgency": signals["urgency"]["score"],
            "churn_risk": signals["churn_risk"]["score"],
            "toxicity": signals["toxicity"]["score"],
            "sarcasm": signals["sarcasm"]["score"]
        }
        return AnalysisResult(radar=radar, classification=classification, voice=voice)
'''
            st.code(pipeline_code, language="python", line_numbers=True)

        # 4. Output JSON
        with code_tab4:
            if res_dict:
                st.code(json.dumps(res_dict, indent=2), language="json")
            else:
                st.info("Run an analysis to inspect the live JSON response contract.")
