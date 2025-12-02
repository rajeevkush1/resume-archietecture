import sys
import os

# Add the current directory to sys.path so we can import utils
sys.path.append(os.getcwd())

from utils.analyzer import analyze_resume

# Dummy Data
resume_text = """
Experienced Python Developer with a strong background in Machine Learning and Data Science.
Proficient in Streamlit, Pandas, and Scikit-Learn.
"""

job_description = """
We are looking for a Senior Python Engineer.
Must have experience with:
- Python
- Machine Learning
- Streamlit
- Data Analysis
"""

print("Running Analysis...")
results = analyze_resume(resume_text, job_description)

print("\n--- Results ---")
print(f"Final Score: {results['final_score']}")
print(f"Keyword Match Score: {results['keyword_match_score']}")
print(f"Semantic Similarity Score: {results['semantic_similarity_score']}")
print(f"Missing Keywords: {results['missing_keywords']}")

# Check types
print("\n--- Types ---")
print(f"Final Score Type: {type(results['final_score'])}")
print(f"Semantic Score Type: {type(results['semantic_similarity_score'])}")
