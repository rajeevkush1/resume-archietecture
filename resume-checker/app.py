import streamlit as st
import os
from utils.parser import extract_text_from_pdf
from utils.analyzer import analyze_resume

import pandas as pd

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
    st.markdown("### 1. Upload Resume(s)")
    uploaded_files = st.file_uploader("Upload your Resume(s) (PDF)", type="pdf", accept_multiple_files=True)
    
    st.markdown("### 2. Job Description")
    job_description = st.text_area("Paste the Job Description here", height=300, placeholder="Paste the JD text here...")
    
    analyze_button = st.button("Analyze Resumes", type="primary", use_container_width=True)

with col2:
    st.markdown("### Analysis Results")
    
    if analyze_button:
        if uploaded_files and job_description:
            with st.spinner("Analyzing resumes..."):
                results_list = []
                
                # Progress bar
                progress_bar = st.progress(0)
                total_files = len(uploaded_files)
                
                for i, uploaded_file in enumerate(uploaded_files):
                    try:
                        # Extract Text
                        resume_text = extract_text_from_pdf(uploaded_file)
                        
                        if resume_text:
                            # Analyze
                            analysis = analyze_resume(resume_text, job_description)
                            
                            # Add filename to results
                            analysis['filename'] = uploaded_file.name
                            results_list.append(analysis)
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                    
                    # Update progress
                    progress_bar.progress((i + 1) / total_files)
                
                if results_list:
                    # Create DataFrame for Ranking
                    df = pd.DataFrame(results_list)
                    
                    # Sort by Final Score
                    df = df.sort_values(by='final_score', ascending=False).reset_index(drop=True)
                    
                    # Display Ranking Table
                    st.markdown("#### 🏆 Candidate Ranking")
                    
                    # Format DataFrame for display
                    display_df = df[['filename', 'final_score', 'keyword_match_score', 'semantic_similarity_score']]
                    display_df.columns = ['Resume Name', 'ATS Score', 'Keyword Match', 'Semantic Score']
                    
                    st.dataframe(
                        display_df.style.background_gradient(subset=['ATS Score'], cmap='Greens'),
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    st.divider()
                    st.markdown("#### 📝 Detailed Analysis")
                    
                    # Detailed View for each resume
                    for index, row in df.iterrows():
                        with st.expander(f"#{index+1} {row['filename']} - Score: {row['final_score']}%"):
                            
                            # Metrics
                            m1, m2, m3 = st.columns(3)
                            with m1:
                                st.metric("ATS Score", f"{row['final_score']}%")
                            with m2:
                                st.metric("Keyword Match", f"{row['keyword_match_score']}%")
                            with m3:
                                st.metric("Semantic Similarity", f"{row['semantic_similarity_score']}%")
                            
                            # Missing Keywords
                            st.markdown("##### ⚠️ Missing Keywords")
                            if row['missing_keywords']:
                                st.markdown("The following important keywords from the JD are missing:")
                                
                                # Display as badges
                                keywords_html = ""
                                for keyword in row['missing_keywords']:
                                    keywords_html += f'<span class="keyword-badge">{keyword}</span>'
                                st.markdown(f'<div class="keyword-container">{keywords_html}</div>', unsafe_allow_html=True)
                            else:
                                st.success("Great job! This resume has all the key keywords.")
                                
                else:
                    st.error("No valid resumes could be processed.")
                    
        else:
            st.warning("Please upload at least one resume and paste a job description.")
    else:
        st.info("Upload resumes and job description to see the ranking.")
        st.markdown("""
        **How it works:**
        1. **Batch Processing:** Upload multiple resumes to compare candidates.
        2. **Ranking:** We rank candidates based on their ATS Match Score.
        3. **Detailed Insights:** Expand each candidate to see missing keywords and detailed scores.
        """)
