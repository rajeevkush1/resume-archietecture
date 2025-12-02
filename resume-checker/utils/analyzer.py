import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import numpy as np

# Load Spacy Model
@st.cache_resource
def load_spacy_model():
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        # If model is not found, download it
        from spacy.cli import download
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    return nlp

# Load Sentence Transformer Model
@st.cache_resource
def load_transformer_model():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

def get_keywords(text, nlp):
    """
    Extracts nouns and proper nouns from the text.
    """
    doc = nlp(text.lower())
    keywords = set([token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]])
    return keywords

def analyze_resume(resume_text, job_description):
    """
    Analyzes the resume against the job description.
    
    Args:
        resume_text (str): Text extracted from the resume.
        job_description (str): Text of the job description.
        
    Returns:
        dict: A dictionary containing the score and missing keywords.
    """
    nlp = load_spacy_model()
    model = load_transformer_model()
    
    # 1. Keyword Match
    jd_keywords = get_keywords(job_description, nlp)
    resume_keywords = get_keywords(resume_text, nlp)
    
    missing_keywords = list(jd_keywords - resume_keywords)
    
    # Calculate Keyword Match Percentage
    if len(jd_keywords) > 0:
        match_percentage = (len(jd_keywords) - len(missing_keywords)) / len(jd_keywords)
    else:
        match_percentage = 0.0
        
    # 2. Semantic Score
    embeddings = model.encode([resume_text, job_description])
    semantic_similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    
    # 3. Final Score Logic
    # Final Score = (Keyword_Match_% * 0.37) + (Semantic_Similarity * 0.63)
    final_score = (match_percentage * 0.37) + (semantic_similarity * 0.63)
    
    # Normalize score to 0-100
    final_score_100 = round(float(final_score * 100), 2)
    
    return {
        "final_score": final_score_100,
        "keyword_match_score": round(float(match_percentage * 100), 2),
        "semantic_similarity_score": round(float(semantic_similarity * 100), 2),
        "missing_keywords": missing_keywords,
        "total_keywords_in_jd": len(jd_keywords),
        "matched_keywords": len(jd_keywords) - len(missing_keywords)
    }
