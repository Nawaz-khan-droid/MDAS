import streamlit as st
import plotly.graph_objects as go
import time
from mdas import MDASAnalyzer

# --- Page Config ---
st.set_page_config(
    page_title="MDAS | Operational Radar",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS for Mesop/Material Design feel ---
st.markdown("""
    <style>
    /* Clean container styling */
    .stApp {
        background-color: #f8f9fa;
        color: #212529;
    }
    .main-container {
        max-width: 900px;
        margin: auto;
    }
    .card {
        background: #ffffff;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
        border: 1px solid #e9ecef;
    }
    .badge-primary {
        background-color: #e7f1ff;
        color: #0d6efd;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 12px;
    }
    .alert-critical {
        background-color: #ffeef0;
        color: #dc3545;
        padding: 12px 16px;
        border-left: 4px solid #dc3545;
        border-radius: 4px;
        font-weight: 600;
        margin-top: 12px;
    }
    .alert-warning {
        background-color: #fff8e6;
        color: #ff9800;
        padding: 12px 16px;
        border-left: 4px solid #ff9800;
        border-radius: 4px;
        font-weight: 600;
        margin-top: 12px;
    }
    .alert-routine {
        background-color: #e7f1ff;
        color: #0d6efd;
        padding: 12px 16px;
        border-left: 4px solid #0d6efd;
        border-radius: 4px;
        font-weight: 600;
        margin-top: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Initialize Global Analyzer Singleton ---
@st.cache_resource(show_spinner="Loading MDAS Engine...")
def get_analyzer():
    return MDASAnalyzer.from_directory("models")

analyzer = get_analyzer()

# --- Main Layout ---
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

st.title("MDAS Operational Radar")
st.markdown("Multi-Dimensional Text Analysis System | Local Baseline V0.1")

# --- Inbound Analysis Control Block ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
text_input = st.text_area(
    "Enter communication to analyze:", 
    height=120, 
    placeholder="e.g. URGENT: The payment failed again, fix this immediately or I am canceling my account!"
)

if st.button("Analyze Communication", type="primary"):
    if not text_input.strip():
        st.warning("Please enter some text.")
    else:
        # Action Trigger: Measure timing
        start_time = time.perf_counter()
        
        # Core execution
        result = analyzer.analyze(text_input).to_dict()
        
        exec_time_ms = (time.perf_counter() - start_time) * 1000
        
        st.markdown("</div>", unsafe_allow_html=True) # close input card
        
        # --- Analytical Profile Display Panel ---
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # Taxonomy Badge
        intent_label = result['classification']['intent']['label'] or "unknown"
        cat_label = result['classification']['category']['label'] or "unknown"
        taxonomy_string = f"taxonomy.{cat_label.lower()}.{intent_label.lower()}"
        st.markdown(f"<div class='badge-primary'>{taxonomy_string}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1.2])
        
        # Radar Data Prep
        radar = result['radar']
        categories = ['Sentiment', 'Urgency', 'Churn Risk', 'Toxicity', 'Sarcasm']
        values = [
            radar['sentiment'], 
            radar['urgency'], 
            radar['churn_risk'], 
            radar['toxicity'], 
            radar['sarcasm']
        ]
        
        with col1:
            st.markdown("#### Dimensional Weights")
            for cat, val in zip(categories, values):
                st.progress(val, text=f"{cat}: {val:.2f}")
                
            st.caption(f"Processed locally in **{exec_time_ms:.2f} ms**")

        with col2:
            # The Radar Metric Visualizer
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]], # close the loop
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(13, 110, 253, 0.2)',
                line=dict(color='#0d6efd', width=2),
                name='Operational Footprint'
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 1])
                ),
                showlegend=False,
                margin=dict(l=30, r=30, t=30, b=30),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
            
        st.markdown("</div>", unsafe_allow_html=True) # close profile card
        
        # --- Operational Automation Log Panel ---
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("#### Action Routing")
        
        urgency = radar['urgency']
        churn = radar['churn_risk']
        
        if urgency >= 0.90:
            st.markdown("<div class='alert-critical'>[CRITICAL ROUTING] Escalated to Live Engineering Queue</div>", unsafe_allow_html=True)
        elif churn >= 0.85:
            st.markdown("<div class='alert-warning'>[RETENTION RISK] Account Manager Notified Via Slack</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='alert-routine'>[AUTOMATION] Logged to Routine Triage Queue</div>", unsafe_allow_html=True)
            
        with st.expander("View Full Raw JSON Contract"):
            st.json(result)
            
        st.markdown("</div>", unsafe_allow_html=True) # close log card

st.markdown("</div>", unsafe_allow_html=True) # close main container
