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

def render_dashboard():
    # --- Theme-Adaptive CSS & Design Token System ---
    st.markdown("""
    <style>
        :root {
            --mdas-slate-900: #1e293b;
            --mdas-slate-600: #475569;
            --mdas-slate-400: #94a3b8;
            --mdas-slate-border: rgba(100, 116, 139, 0.18);
            --mdas-surface: var(--secondary-background-color);
            --mdas-safe: #059669;        /* emerald, 0.0 baseline */
            --mdas-caution: #d97706;     /* amber, mid-risk */
            --mdas-critical: #b91c1c;    /* muted crimson, >0.75 */
            --mdas-accent: #334155;      /* neutral structural accent */
        }

        /* Prevent global horizontal overflow */
        .stApp {
            overflow-x: hidden;
            max-width: 1440px;
            margin: 0 auto;
        }

        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--mdas-slate-border);
            padding-bottom: 10px;
            margin-bottom: 18px;
        }
        .pane-title {
            font-size: 0.82rem;
            font-weight: 650;
            letter-spacing: 1.1px;
            text-transform: uppercase;
            color: var(--mdas-slate-600);
        }
        .status-badge {
            background-color: rgba(5, 150, 105, 0.10);
            color: var(--mdas-safe);
            border: 1px solid rgba(5, 150, 105, 0.25);
            padding: 3px 10px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 0.72rem;
            letter-spacing: 0.3px;
        }

        /* --- KPI Grid: Single Flexbox Container --- */
        .kpi-grid {
            display: flex;
            flex-direction: row;
            gap: 8px;
            width: 100%;
            margin-top: 8px;
            margin-bottom: 14px;
        }
        .kpi-card {
            flex: 1 1 0px;
            min-width: 0;
            background-color: var(--mdas-surface);
            border: 1px solid var(--mdas-slate-border);
            border-top: 3px solid transparent;
            border-radius: 6px;
            padding: 10px 10px 8px 10px;
            text-align: left;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }
        .kpi-card.risk-safe     { border-top-color: var(--mdas-safe); }
        .kpi-card.risk-caution  { border-top-color: var(--mdas-caution); }
        .kpi-card.risk-critical { border-top-color: var(--mdas-critical); }

        .kpi-eyebrow {
            font-size: 0.62rem;
            text-transform: uppercase;
            font-weight: 650;
            letter-spacing: 0.5px;
            color: var(--mdas-slate-400);
            margin-bottom: 4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .kpi-value {
            font-size: 1.15rem;
            font-weight: 650;
            color: var(--mdas-slate-900);
            line-height: 1.2;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .kpi-sub {
            font-size: 0.68rem;
            font-weight: 500;
            color: var(--mdas-slate-400);
            margin-top: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* --- Action Banners --- */
        .action-box {
            padding: 14px 16px;
            border-radius: 6px;
            margin-top: 14px;
            margin-bottom: 14px;
            font-weight: 500;
            display: flex;
            align-items: flex-start;
            gap: 12px;
            font-size: 0.88rem;
            border: 1px solid var(--mdas-slate-border);
        }
        .action-critical { background-color: rgba(185, 28, 28, 0.06); border-left: 3px solid var(--mdas-critical); color: var(--mdas-critical); }
        .action-warning  { background-color: rgba(217, 119, 6, 0.06); border-left: 3px solid var(--mdas-caution); color: var(--mdas-caution); }
        .action-routine  { background-color: rgba(51, 65, 85, 0.05); border-left: 3px solid var(--mdas-accent); color: var(--mdas-slate-600); }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
            margin-top: 5px;
            flex-shrink: 0;
        }
        .dot-critical { background-color: var(--mdas-critical); box-shadow: 0 0 0 2px rgba(185, 28, 28, 0.2); }
        .dot-warning  { background-color: var(--mdas-caution);  box-shadow: 0 0 0 2px rgba(217, 119, 6, 0.2); }
        .dot-routine  { background-color: var(--mdas-accent);   box-shadow: 0 0 0 2px rgba(51, 65, 85, 0.2); }

        .tag-chip {
            display: inline-block;
            padding: 3px 9px;
            border-radius: 4px;
            font-size: 0.74rem;
            font-weight: 550;
            background-color: rgba(100, 116, 139, 0.08);
            border: 1px solid var(--mdas-slate-border);
            color: var(--mdas-slate-600);
            margin: 2px 4px 2px 0;
        }

        /* --- Button as Flat Card Launcher --- */
        .stButton > button {
            border-radius: 6px !important;
            border: 1px solid var(--mdas-slate-border) !important;
            background-color: var(--mdas-surface) !important;
            color: var(--mdas-slate-900) !important;
            font-weight: 550 !important;
            font-size: 0.80rem !important;
            padding: 7px 10px !important;
            text-align: center !important;
            transition: all 0.15s ease !important;
        }
        .stButton > button:hover {
            border-color: var(--mdas-slate-400) !important;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08) !important;
        }
        .stButton > button[kind="primary"] {
            background-color: var(--mdas-accent) !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            padding: 10px 16px !important;
        }

        /* Force KPI text to wrap instead of ellipsis-truncating if a
           label is ever longer than the card at narrow widths */
        .kpi-eyebrow, .kpi-value, .kpi-sub {
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: unset !important;
            word-break: break-word;
        }

        /* Equal-height cards regardless of value/label length */
        .kpi-card {
            min-height: 92px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Initialize Global MDAS Engine ---
    @st.cache_resource(show_spinner="Initializing MDAS Engine...")
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
        "Urgent Outage": "URGENT: Production payment gateway is down and throwing 500 errors. Fix this immediately or I am canceling our enterprise agreement today!",
        "Churn Risk": "I am deeply disappointed with the latest software update. The UI is clunky and slow. We are seriously evaluating switching to your competitor next month.",
        "Billing Inquiry": "Hello support team, could you please explain why our invoice #84920 includes a 15% recurring cloud surcharge? Thank you.",
        "Sarcastic Feedback": "Oh brilliant engineering work, team. Deploying breaking database migrations on Friday evening without testing is truly a masterclass in QA.",
        "Phishing Spam": "CONGRATULATIONS WINNER! You have won an exclusive $5,000 Apple Gift Card. Click here now to verify your credentials before this prize expires!",
        "Rave Review": "I am absolutely thrilled with this tool! The latency is lightning fast and our entire engineering workflow has doubled in productivity."
    }

    # --- Sidebar Controls ---
    st.sidebar.markdown("### Layout Settings")
    show_code_pane = st.sidebar.checkbox("Show Command Palette", value=True)
    split_ratio = st.sidebar.radio("Split Mode", ["50 / 50", "60 / 40", "Preview Only"], index=0)

    # --- Top Navigation Bar ---
    top_left, top_right = st.columns([1.1, 1] if show_code_pane and split_ratio != "Preview Only" else [1, 0.001])
    with top_left:
        st.markdown("""
        <div class="top-bar">
            <div class="pane-title">Preview</div>
            <div class="status-badge">Engine Online (v0.1.0)</div>
        </div>
        """, unsafe_allow_html=True)

    if show_code_pane and split_ratio != "Preview Only":
        with top_right:
            st.markdown("""
            <div class="top-bar">
                <div class="pane-title">Command Palette</div>
                <div style="font-size: 0.74rem; color: var(--mdas-slate-400); font-weight: 550;">PYTHON • REST • CONTRACTS</div>
            </div>
            """, unsafe_allow_html=True)

    # --- Layout Grid ---
    if show_code_pane and split_ratio == "50 / 50":
        col_preview, col_code = st.columns([1, 1])
    elif show_code_pane and split_ratio == "60 / 40":
        col_preview, col_code = st.columns([1.3, 1])
    else:
        col_preview = st.container()
        col_code = None

    # ==========================================
    # LEFT PANE: PREVIEW & INTERACTION
    # ==========================================
    with col_preview:
        st.markdown("### MDAS Operational Radar")
        st.caption("Multi-Dimensional Text Analysis System • Modular Monolith V0.1 • Fast Offline NLP")

        # Quick Samples Grid (Single-Element Card Buttons)
        st.markdown("<div class='kpi-eyebrow' style='margin-top:10px;'>Quick Example Prompts</div>", unsafe_allow_html=True)
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
        st.write("")
        input_text = st.text_area(
            "Communication payload to analyze:",
            value=current_prompt,
            height=90,
            placeholder="Type or paste any customer communication, support ticket, review, or email..."
        )

        run_btn = st.button("Run Multi-Dimensional Analysis", type="primary", use_container_width=True)

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

            # Hierarchy-First KPI Cards v2 (Unified Flexbox Grid)
            sent_risk = "risk-safe" if sentiment_label == "Positive" else "risk-critical" if sentiment_label == "Negative" else ""
            is_spam = spam_label.lower() == "spam"
            spam_risk = "risk-critical" if is_spam else "risk-safe"
            
            st.markdown(f"""
            <div class="kpi-grid">
                <div class="kpi-card {sent_risk}">
                    <div class="kpi-eyebrow">Sentiment</div>
                    <div class="kpi-value">{sentiment_label}</div>
                    <div class="kpi-sub">Polarity {sentiment_score:.2f}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-eyebrow">Intent</div>
                    <div class="kpi-value">{intent_label}</div>
                    <div class="kpi-sub">Model-classified</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-eyebrow">Category</div>
                    <div class="kpi-value">{cat_label}</div>
                    <div class="kpi-sub">Routing vertical</div>
                </div>
                <div class="kpi-card {spam_risk}">
                    <div class="kpi-eyebrow">Security</div>
                    <div class="kpi-value">{'Spam' if is_spam else 'Authentic'}</div>
                    <div class="kpi-sub">{'Flagged payload' if is_spam else 'Verified clean'}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-eyebrow">Latency</div>
                    <div class="kpi-value">{latency_ms:.2f} ms</div>
                    <div class="kpi-sub">Local CPU</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Precise Operational Action Dispatch Banner
            if urgency_score >= 0.67 and churn_score >= 0.70:
                st.markdown(f"""
                <div class="action-box action-critical">
                    <span class="status-dot dot-critical"></span>
                    <div>
                        <strong>CRITICAL DISPATCH: SRE Incident Response & Executive Retention Escalation</strong><br/>
                        Severe operational outage and high churn risk detected (Urgency: {urgency_score:.2f}, Churn Risk: {churn_score:.2f}). Escalated to Senior SRE & Retention Taskforce.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif urgency_score >= 0.67:
                st.markdown(f"""
                <div class="action-box action-critical">
                    <span class="status-dot dot-critical"></span>
                    <div>
                        <strong>CRITICAL DISPATCH: Senior SRE Priority Incident Response</strong><br/>
                        High urgency infrastructure/service impact detected (Urgency: {urgency_score:.2f}). Dispatched directly to On-Call Engineering.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif churn_score >= 0.70:
                st.markdown(f"""
                <div class="action-box action-warning">
                    <span class="status-dot dot-warning"></span>
                    <div>
                        <strong>RETENTION ALERT: Account Management Review</strong><br/>
                        Elevated customer churn probability detected (Churn Risk: {churn_score:.2f}). Flagged for Customer Success retention intervention.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif toxicity_score >= 0.50:
                st.markdown(f"""
                <div class="action-box action-warning">
                    <span class="status-dot dot-warning"></span>
                    <div>
                        <strong>CONTENT MODERATION: Staff Well-Being Review</strong><br/>
                        Elevated toxicity score ({toxicity_score:.2f}). Flagged for policy compliance and employee protection.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif urgency_score >= 0.34:
                st.markdown(f"""
                <div class="action-box action-warning">
                    <span class="status-dot dot-warning"></span>
                    <div>
                        <strong>TIER-2 ROUTING: Specialized {cat_label} Queue</strong><br/>
                        Moderate priority communication (Urgency: {urgency_score:.2f}). Assigned to domain specialists for expedited triage.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="action-box action-routine">
                    <span class="status-dot dot-routine"></span>
                    <div>
                        <strong>ROUTINE TRIAGE: Standard Automation</strong><br/>
                        Low-risk baseline communication. Queued for standard automated workflow processing.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Radar & Signals
            r_col1, r_col2 = st.columns([1.1, 1])
            with r_col1:
                st.markdown("##### Operational Radar")
                radar_cats = ['Sentiment (Neg)', 'Urgency', 'Churn Risk', 'Toxicity', 'Sarcasm']
                radar_vals = [sentiment_score, urgency_score, churn_score, toxicity_score, sarcasm_score]

                fig = go.Figure()
                is_high_risk = urgency_score > 0.6 or churn_score > 0.6 or toxicity_score > 0.5
                line_color = "#b91c1c" if is_high_risk else "#334155"
                fill_color = "rgba(185, 28, 28, 0.10)" if is_high_risk else "rgba(51, 65, 85, 0.10)"

                fig.add_trace(go.Scatterpolar(
                    r=radar_vals + [radar_vals[0]],
                    theta=radar_cats + [radar_cats[0]],
                    fill='toself',
                    fillcolor=fill_color,
                    line=dict(color=line_color, width=2),
                    name='Operational Footprint'
                ))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 1],
                            tickvals=[0, 0.25, 0.5, 0.75, 1.0],
                            showticklabels=True,
                            tickfont=dict(size=9, color="#94a3b8"),
                            ticks='',
                            gridcolor='rgba(100, 116, 139, 0.15)',
                            linecolor='rgba(100, 116, 139, 0.15)'
                        ),
                        angularaxis=dict(
                            gridcolor='rgba(100, 116, 139, 0.15)',
                            tickfont=dict(size=10.5, color="#475569")
                        ),
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    margin=dict(l=30, r=30, t=20, b=20),
                    height=280
                )
                st.plotly_chart(fig, use_container_width=True)

            with r_col2:
                st.markdown("##### Behavioral Risk Signals")
                def show_signal(title, val, label, ev_count):
                    color = "#059669" if val < 0.34 else "#d97706" if val < 0.67 else "#b91c1c"
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px;">
                        <span><strong>{title}</strong></span>
                        <span style="color: {color}; font-weight: 700; font-size: 0.85rem;">{label.upper()} ({val:.2f})</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(float(val))
                    if ev_count:
                        st.caption(f"Trigger evidence count: {ev_count}")

                show_signal("Urgency", urgency_score, signals.get("urgency", {}).get("label", "low"), signals.get("urgency", {}).get("evidence_count", 0))
                show_signal("Churn Risk", churn_score, signals.get("churn_risk", {}).get("label", "low"), signals.get("churn_risk", {}).get("evidence_count", 0))
                show_signal("Toxicity", toxicity_score, signals.get("toxicity", {}).get("label", "low"), signals.get("toxicity", {}).get("evidence_count", 0))
                show_signal("Sarcasm", sarcasm_score, signals.get("sarcasm", {}).get("label", "low"), signals.get("sarcasm", {}).get("marker_count", 0))

            # Linguistic & Voice Breakdown
            with st.expander("Deep Linguistic Analysis & Grammatical Voice", expanded=False):
                ling_c1, ling_c2 = st.columns(2)
                with ling_c1:
                    st.markdown("**Grammatical Voice Analysis:**")
                    voice_summary = ling.get("voice", {}).get("summary", {})
                    st.write(f"- Active Sentences: `{voice_summary.get('active', 0)}`")
                    st.write(f"- Passive Sentences: `{voice_summary.get('passive', 0)}`")
                    st.write(f"- Uncertain Sentences: `{voice_summary.get('uncertain', 0)}`")
                    
                    sentences = ling.get("voice", {}).get("sentences", [])
                    for s in sentences:
                        st.markdown(f"- *\"{s.get('text')}\"* → **{s.get('voice')} Voice** (`Subject: {s.get('subject') or 'None'}`) [{s.get('reason')}]")

                with ling_c2:
                    st.markdown("**Extracted Named Entities & Identifiers:**")
                    entities = ling.get("entities", [])
                    if entities:
                        chips = "".join([f"<span class='tag-chip'>{e.get('text')} ({e.get('label')})</span>" for e in entities])
                        st.markdown(chips, unsafe_allow_html=True)
                    else:
                        st.info("No named entities detected.")

                    st.markdown("**Text Statistics & Readability:**")
                    st.write(f"- Total Words: `{stats.get('words', 0)}` | Sentences: `{stats.get('sentences', 0)}`")
                    st.write(f"- Lexical Diversity (TTR): `{stats.get('lexical_diversity', 0):.2f}`")

        else:
            st.info("💡 Enter text above or choose a quick prompt to trigger the multi-dimensional analysis.")
            res_dict = None
            input_text = ""

    # ==========================================
    # RIGHT PANE: COMMAND PALETTE
    # ==========================================
    if col_code:
        with col_code:
            code_tab1, code_tab2, code_tab3, code_tab4 = st.tabs([
                "Python Client", 
                "REST API", 
                "App Architecture", 
                "Output JSON"
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
                st.code(python_sdk_code, language="python", line_numbers=True, height=480, wrap_lines=False)

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
                st.code(rest_code, language="python", line_numbers=True, height=480, wrap_lines=False)

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
                st.code(pipeline_code, language="python", line_numbers=True, height=480, wrap_lines=False)

            # 4. Output JSON (Clean, High-Signal Contract)
            with code_tab4:
                if res_dict:
                    clean_contract = {
                        "radar": radar,
                        "classification": {
                            k: {
                                "label": v.get("label"),
                                "confidence": round(v.get("confidence", 0.0), 3) if v.get("confidence") is not None else None,
                                "alternatives": {alt_k: round(alt_v, 3) for alt_k, alt_v in v.get("alternatives", {}).items()} if isinstance(v.get("alternatives"), dict) else v.get("alternatives")
                            }
                            for k, v in classification.items()
                            if v.get("status") == "ok" and v.get("label") is not None
                        },
                        "signals": {
                            k: {
                                "score": round(v.get("score", 0.0), 3),
                                "label": v.get("label"),
                                "evidence_count": v.get("evidence_count", 0) if "evidence_count" in v else v.get("marker_count", 0)
                            }
                            for k, v in signals.items()
                        },
                        "voice": {
                            "summary": ling.get("voice", {}).get("summary"),
                            "sentences": [
                                {
                                    "text": s.get("text"),
                                    "voice": s.get("voice"),
                                    "subject": s.get("subject"),
                                    "verb": s.get("verb"),
                                    "confidence": s.get("confidence")
                                }
                                for s in ling.get("voice", {}).get("sentences", [])
                            ]
                        },
                        "entities": [
                            {"text": e.get("text"), "label": e.get("label")}
                            for e in ling.get("entities", [])
                        ],
                        "statistics": {
                            "words": stats.get("words"),
                            "sentences": stats.get("sentences"),
                            "lexical_diversity": stats.get("lexical_diversity"),
                            "inference_latency_ms": round(latency_ms, 2)
                        }
                    }
                    st.code(json.dumps(clean_contract, indent=2), language="json", height=480, wrap_lines=False)
                else:
                    st.info("Run an analysis to inspect the live JSON response contract.")

# --- Multi-Page Routing via st.navigation ---
try:
    dashboard_page = st.Page(render_dashboard, title="Dashboard", icon="🧭", default=True)
    docs_page = st.Page("pages/Docs.py", title="Docs", icon="📖")
    settings_page = st.Page("pages/Settings.py", title="Settings", icon="⚙️")

    pg = st.navigation([dashboard_page, docs_page, settings_page])
    pg.run()
except AttributeError:
    # Fallback for older Streamlit versions
    render_dashboard()
