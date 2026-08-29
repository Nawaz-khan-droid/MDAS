import streamlit as st
import plotly.graph_objects as go
import time
from mdas import MDASAnalyzer

# --- Page Configuration ---
st.set_page_config(
    page_title="MDAS | Operational Text Radar",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Theme-Aware & Adaptive CSS ---
st.markdown("""
<style>
    /* Metric Cards */
    .metric-box {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        margin-bottom: 12px;
    }
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        opacity: 0.7;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--text-color);
    }
    
    /* Signal Item */
    .signal-card {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    
    /* Dynamic Action Alerts */
    .action-alert {
        padding: 16px 20px;
        border-radius: 8px;
        margin-top: 12px;
        margin-bottom: 16px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .action-critical {
        background-color: rgba(239, 68, 68, 0.15);
        border-left: 5px solid #ef4444;
        color: #ef4444;
    }
    .action-warning {
        background-color: rgba(245, 158, 11, 0.15);
        border-left: 5px solid #f59e0b;
        color: #f59e0b;
    }
    .action-routine {
        background-color: rgba(59, 130, 246, 0.15);
        border-left: 5px solid #3b82f6;
        color: #3b82f6;
    }
    
    /* Pill Tag */
    .tag-pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        background-color: rgba(128, 128, 128, 0.15);
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Global Analyzer Singleton ---
@st.cache_resource(show_spinner="Initializing MDAS NLP Engine & Model Registry...")
def get_analyzer():
    return MDASAnalyzer.from_directory("models")

try:
    analyzer = get_analyzer()
    engine_ready = True
except Exception as e:
    engine_ready = False
    init_error = str(e)

# --- Header Section ---
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.title("🧭 MDAS Operational Radar")
    st.caption("Multi-Dimensional Text Analysis System • Modular Monolith V0.1 • Fast Offline NLP")
with header_col2:
    if engine_ready:
        st.markdown(
            "<div style='text-align: right; margin-top: 15px;'>"
            "<span style='background-color: rgba(16, 185, 129, 0.2); color: #10b981; padding: 6px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem;'>● Engine Online</span>"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        st.error("Engine Offline")

if not engine_ready:
    st.error(f"Failed to load engine: {init_error}")
    st.stop()

# --- Sample Selection ---
sample_texts = {
    "🚨 Urgent Churn Risk": "URGENT: Your latest software update broke my entire billing system. Fix this right now or I am canceling my subscription and switching to your competitor immediately!",
    "💬 Billing Inquiry": "Hi support team, could you please provide a breakdown of the transaction charges on our last invoice #4928? Thanks!",
    "⚠️ Sarcastic Dissatisfaction": "Oh brilliant job team, another failed deployment right before the weekend. Truly stellar quality assurance.",
    "🛡️ Spam / Phishing Payload": "CONGRATULATIONS! You have won a $1,000 Walmart Gift Card. Click here immediately to claim your prize before it expires today!",
    "🌟 Enthusiastic Feedback": "I absolutely love this product! The speed and interface are fantastic. Keep up the amazing work!"
}

st.write("")
col_samp_label, col_samps = st.columns([1, 5])
with col_samp_label:
    st.markdown("**Quick Samples:**")
with col_samps:
    btn_cols = st.columns(len(sample_texts))
    for i, (name, text) in enumerate(sample_texts.items()):
        if btn_cols[i].button(name.split()[0] + " " + name.split()[1], key=f"samp_{i}", help=text):
            st.session_state["input_text"] = text

default_val = st.session_state.get(
    "input_text", 
    "URGENT: Your payment portal failed again! Fix this immediately or I am canceling our enterprise account."
)

# --- Input Area ---
text_input = st.text_area(
    "Enter communication text to analyze:", 
    value=default_val, 
    height=110,
    placeholder="Type or paste any customer communication, support ticket, or feedback..."
)

analyze_btn = st.button("⚡ Run Multi-Dimensional Analysis", type="primary", use_container_width=True)

if text_input.strip():
    # Execute Pipeline
    start_time = time.perf_counter()
    res = analyzer.analyze(text_input)
    exec_time_ms = (time.perf_counter() - start_time) * 1000
    data = res.to_dict()
    
    radar = data.get("radar", {})
    signals = data.get("signals", {})
    classification = data.get("classification", {})
    stats = data.get("statistics", {})
    ling = data.get("linguistics", {})
    
    sentiment_label = (classification.get("sentiment", {}).get("label") or "Neutral").capitalize()
    intent_label = (classification.get("intent", {}).get("label") or "General").capitalize()
    cat_label = (classification.get("category", {}).get("label") or "Support").capitalize()
    spam_label = (classification.get("spam", {}).get("label") or "Ham").capitalize()
    
    urgency_val = radar.get("urgency", 0.0)
    churn_val = radar.get("churn_risk", 0.0)
    toxicity_val = radar.get("toxicity", 0.0)
    sarcasm_val = radar.get("sarcasm", 0.0)
    sentiment_val = radar.get("sentiment", 0.5)

    st.write("")
    
    # --- Top KPI Summary Ribbon ---
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>Sentiment</div>
            <div class='metric-value'>{'🟢 Positive' if sentiment_label=='Positive' else '🔴 Negative' if sentiment_label=='Negative' else '⚪ Neutral'}</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>Primary Intent</div>
            <div class='metric-value'>{intent_label}</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>Category Domain</div>
            <div class='metric-value'>{cat_label}</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi4:
        is_spam = spam_label.lower() == "spam"
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>Security / Spam</div>
            <div class='metric-value'>{'🚨 Spam' if is_spam else '✅ Authentic'}</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi5:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>Local Latency</div>
            <div class='metric-value'>{exec_time_ms:.2f} ms</div>
        </div>
        """, unsafe_allow_html=True)

    # --- Operational Action Routing Alert ---
    if urgency_val >= 0.67 or churn_val >= 0.85:
        st.markdown(
            f"""
            <div class='action-alert action-critical'>
                <span style='font-size: 1.5rem;'>🚨</span>
                <div>
                    <strong>CRITICAL AUTOMATION DISPATCH:</strong> High operational risk detected 
                    (Urgency: {urgency_val:.2f}, Churn Risk: {churn_val:.2f}). 
                    Escalated directly to Priority Response & Retention Queue.
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    elif toxicity_val >= 0.50:
        st.markdown(
            f"""
            <div class='action-alert action-warning'>
                <span style='font-size: 1.5rem;'>⚠️</span>
                <div>
                    <strong>CONTENT MODERATION WARNING:</strong> Elevated toxicity signal ({toxicity_val:.2f}). 
                    Flagged for staff well-being review and policy moderation.
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    elif urgency_val >= 0.34 or churn_val >= 0.34:
        st.markdown(
            f"""
            <div class='action-alert action-warning'>
                <span style='font-size: 1.5rem;'>🔔</span>
                <div>
                    <strong>ATTENTION ROUTING:</strong> Moderate priority query. Routed to specialized {cat_label} tier-2 queue.
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class='action-alert action-routine'>
                <span style='font-size: 1.5rem;'>ℹ️</span>
                <div>
                    <strong>ROUTINE AUTOMATION:</strong> Standard workflow triage. Queued for normal automated processing.
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # --- Main Analysis Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 5-Axis Radar & Signals", 
        "🏷️ Classifiers & Probabilities", 
        "🔍 Linguistics & Voice", 
        "📜 Developer JSON Contract"
    ])
    
    # === TAB 1: Radar & Risk Signals ===
    with tab1:
        col_radar, col_signals = st.columns([1.1, 1])
        
        with col_radar:
            st.markdown("#### 🧭 Operational Risk Radar")
            categories = ['Sentiment (Neg)', 'Urgency', 'Churn Risk', 'Toxicity', 'Sarcasm']
            values = [sentiment_val, urgency_val, churn_val, toxicity_val, sarcasm_val]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(239, 68, 68, 0.25)' if (urgency_val > 0.6 or churn_val > 0.6) else 'rgba(59, 130, 246, 0.25)',
                line=dict(
                    color='#ef4444' if (urgency_val > 0.6 or churn_val > 0.6) else '#3b82f6', 
                    width=2.5
                ),
                name='Signal Profile'
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
                        tickfont=dict(size=12, family="sans-serif")
                    ),
                    bgcolor='rgba(0,0,0,0)'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(l=40, r=40, t=30, b=30),
                height=340
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Radar scale maps operational risk intensity from 0.0 (baseline calm) to 1.0 (critical emergency).")

        with col_signals:
            st.markdown("#### 🎯 Behavioral Risk Signals")
            
            def render_signal_bar(name, score, label, evidence_count=0, icon=""):
                color = "green" if score < 0.34 else "orange" if score < 0.67 else "red"
                st.markdown(f"""
                <div style='margin-bottom: 12px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;'>
                        <span><strong>{icon} {name}</strong></span>
                        <span class='tag-pill' style='color: {color}; border: 1px solid {color};'>{label.upper()} ({score:.2f})</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(float(score))
                if evidence_count:
                    st.caption(f"Found {evidence_count} lexical trigger markers in communication.")

            render_signal_bar("Urgency", urgency_val, signals.get("urgency", {}).get("label", "low"), signals.get("urgency", {}).get("evidence_count", 0), "⚡")
            render_signal_bar("Churn Risk", churn_val, signals.get("churn_risk", {}).get("label", "low"), signals.get("churn_risk", {}).get("evidence_count", 0), "🚪")
            render_signal_bar("Toxicity", toxicity_val, signals.get("toxicity", {}).get("label", "low"), signals.get("toxicity", {}).get("evidence_count", 0), "☣️")
            render_signal_bar("Sarcasm", sarcasm_val, signals.get("sarcasm", {}).get("label", "low"), signals.get("sarcasm", {}).get("marker_count", 0), "🎭")

    # === TAB 2: Classifiers & Probabilities ===
    with tab2:
        st.markdown("#### 🏷️ Scikit-Learn Model Registry Classifications")
        
        c_cols = st.columns(2)
        tasks = [("intent", "Intent Classifier", "🎯"), ("category", "Category Classifier", "📂"), ("sentiment", "Sentiment Classifier", "❤️"), ("spam", "Spam & Security Filter", "🛡️")]
        
        for idx, (task_key, task_title, task_icon) in enumerate(tasks):
            col_target = c_cols[idx % 2]
            with col_target:
                task_data = classification.get(task_key, {})
                status = task_data.get("status", "unknown")
                label = task_data.get("label")
                conf = task_data.get("confidence")
                model_name = task_data.get("model", "TF-IDF + LinearSVC")
                
                with st.container():
                    st.markdown(f"##### {task_icon} {task_title}")
                    if status == "model_unavailable":
                        st.info("Model not trained or unavailable.")
                    else:
                        conf_pct = f"{conf*100:.1f}%" if conf is not None else "N/A"
                        st.write(f"**Predicted Label:** `{label}`")
                        st.write(f"**Confidence:** `{conf_pct}` | **Model:** `{model_name}`")
                        
                        alts = task_data.get("alternatives")
                        if alts and isinstance(alts, dict):
                            with st.expander("Candidate Class Probabilities"):
                                for alt_k, alt_v in alts.items():
                                    st.progress(float(alt_v), text=f"{alt_k}: {alt_v*100:.1f}%")
                    st.divider()

    # === TAB 3: Linguistics & Voice ===
    with tab3:
        st.markdown("#### 🔍 Syntax, Voice & Named Entity Recognition")
        
        l_col1, l_col2 = st.columns(2)
        
        with l_col1:
            st.markdown("##### 🗣️ Grammatical Voice Analysis")
            voice_summary = ling.get("voice", {}).get("summary", {})
            active_cnt = voice_summary.get("active", 0)
            passive_cnt = voice_summary.get("passive", 0)
            uncertain_cnt = voice_summary.get("uncertain", 0)
            
            v_col1, v_col2, v_col3 = st.columns(3)
            v_col1.metric("Active Sentences", active_cnt)
            v_col2.metric("Passive Sentences", passive_cnt)
            v_col3.metric("Uncertain", uncertain_cnt)
            
            sentences = ling.get("voice", {}).get("sentences", [])
            if sentences:
                st.write("**Sentence Breakdown:**")
                for s in sentences:
                    st.markdown(f"- *\"{s.get('text')}\"* → **{s.get('voice')} Voice** (`Subject: {s.get('subject') or 'None'}`, `Verb: {s.get('verb') or 'None'}`)")
            
            st.markdown("##### 📊 Document Statistics")
            st.write(f"- **Words:** {stats.get('words', 0)} ({stats.get('alphabetic_words', 0)} alphabetic)")
            st.write(f"- **Sentences:** {stats.get('sentences', 0)} (Avg {stats.get('average_words_per_sentence', 0):.1f} words/sent)")
            st.write(f"- **Lexical Diversity (TTR):** {stats.get('lexical_diversity', 0):.2f}")
            st.write(f"- **Characters:** {stats.get('characters', 0)}")

        with l_col2:
            st.markdown("##### 🏷️ Extracted Named Entities")
            entities = ling.get("entities", [])
            if entities:
                for ent in entities:
                    st.markdown(f"<span class='tag-pill' style='font-size: 0.9rem; margin-bottom: 8px;'>🏷️ <strong>{ent.get('text')}</strong> ({ent.get('label')})</span>", unsafe_allow_html=True)
            else:
                st.info("No specific named entities (people, organizations, dates, locations) found in text.")
                
            st.markdown("##### 🔤 Top Lemmas / Root Words")
            top_lemmas = ling.get("top_lemmas", [])[:8]
            if top_lemmas:
                lemma_chips = " ".join([f"<span class='tag-pill'>{item['lemma']} ({item['count']})</span>" for item in top_lemmas])
                st.markdown(lemma_chips, unsafe_allow_html=True)

    # === TAB 4: Developer JSON Contract ===
    with tab4:
        st.markdown("#### 📜 Standardized AnalysisResult JSON Contract")
        st.caption("This full JSON schema is consumed by downstream APIs, microservices, and databases.")
        st.json(data)

else:
    st.info("💡 Enter text above or click one of the quick samples to run the multi-dimensional analysis.")

