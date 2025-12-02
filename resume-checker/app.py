import streamlit as st
import os
from utils.parser import extract_text_from_pdf
from utils.analyzer import analyze_resume

# Page Configuration
st.set_page_config(
    page_title="AI Resume Checker & ATS Scanner",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Path to CSS
css_path = os.path.join(os.path.dirname(__file__), 'assets', 'style.css')
if os.path.exists(css_path):
    load_css(css_path)

# Header
st.markdown("""
<div class="main-header">
    <h1>AI Resume Checker & ATS Scanner</h1>
    <p>Optimize your resume for Applicant Tracking Systems with AI-powered analysis.</p>
</div>
""", unsafe_allow_html=True)

# Main Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 1. Upload Resume")
    uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")
    
    st.markdown("### 2. Job Description")
    job_description = st.text_area("Paste the Job Description here", height=300, placeholder="Paste the JD text here...")
    
    analyze_button = st.button("Analyze Resume", type="primary", use_container_width=True)

with col2:
    st.markdown("### Analysis Results")
    
    if analyze_button:
        if uploaded_file is not None and job_description:
            with st.spinner("Analyzing your resume..."):
                try:
                    # Extract Text
                    resume_text = extract_text_from_pdf(uploaded_file)
                    
                    if not resume_text:
                        st.error("Could not extract text from the PDF. Please try another file.")
                    else:
                        # Analyze
                        results = analyze_resume(resume_text, job_description)
                        
                        # Display Score
                        st.markdown(f"""
                        <div class="score-card">
                            <div class="score-label">ATS Match Score</div>
                            <div class="score-value">{results['final_score']}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Detailed Metrics
                        m1, m2 = st.columns(2)
                        with m1:
                            st.metric("Keyword Match", f"{results['keyword_match_score']}%")
                        with m2:
                            st.metric("Semantic Similarity", f"{results['semantic_similarity_score']}%")
                        
                        st.divider()
                        
                        # Missing Keywords
                        st.markdown("#### ⚠️ Missing Keywords")
                        if results['missing_keywords']:
                            st.markdown("The following important keywords from the JD are missing in your resume:")
                            
                            # Display as badges
                            keywords_html = ""
                            for keyword in results['missing_keywords']:
                                keywords_html += f'<span class="keyword-badge">{keyword}</span>'
                            st.markdown(f'<div class="keyword-container">{keywords_html}</div>', unsafe_allow_html=True)
                        else:
                            st.success("Great job! You have all the key keywords.")
                            
                except Exception as e:
                    st.error(f"An error occurred during analysis: {str(e)}")
                    st.exception(e)
        else:
            st.warning("Please upload a resume and paste a job description to proceed.")
    else:
        st.info("Upload a resume and job description to see the analysis.")
        st.markdown("""
        **How it works:**
        1. **Keyword Match:** We check if your resume contains specific nouns and skills from the JD.
        2. **Semantic Similarity:** We use **AI (Sentence Transformers)** to understand the *meaning* of your experience compared to the job requirements.
           * *Why Transformers?* Unlike simple keyword matching, transformers understand context. For example, they know that "ML Engineer" and "Data Scientist" are related roles, even if the words are different.
        """)
