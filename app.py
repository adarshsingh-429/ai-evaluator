import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from meta_evaluator import MetaEvaluator

st.set_page_config(page_title="Meta-AI Evaluator", page_icon="🌐", layout="wide")

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
    }
    .main-header h1 {
        background: linear-gradient(135deg, #00f5ff, #7b2dff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
    }
</style>
<div class="main-header">
    <h1>🌐 META-AI EVALUATOR</h1>
    <p>Live Fact-Checking from Wikipedia & Web</p>
</div>
""", unsafe_allow_html=True)

evaluator = MetaEvaluator()

question = st.text_input("Your Question", "When was the Eiffel Tower built and who designed it?")
response = st.text_area("AI Response to Evaluate (optional)", "The Eiffel Tower was built in 1850 by Leonardo da Vinci.")

if st.button("🚀 Evaluate & Correct", type="primary"):
    with st.spinner("🔍 Fetching live facts from Wikipedia..."):
        report = evaluator.evaluate_and_correct(question, response if response else None)
    
    eval_data = report["evaluation"]
    score = eval_data["overall_score"]
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Overall Score", f"{score}/5.0")
    col2.metric("Facts Found", eval_data["facts_found"])
    col3.metric("Accuracy", f"{eval_data['accuracy']}/5")
    col4.metric("Relevance", f"{eval_data['relevance']}/5")
    
    st.subheader("📚 Reference Facts")
    for fact in report["reference_facts"]:
        st.info(fact)
    
    if report["corrected_answer"] != report["original_response"]:
        st.subheader("✅ Corrected Answer")
        st.success(report["corrected_answer"])
    else:
        st.success("No corrections needed - answer is accurate!")
