# AI Resume Checker & ATS Scanner 📄

An intelligent resume analysis tool powered by AI that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS). This application uses advanced Natural Language Processing (NLP) and Machine Learning techniques to provide detailed feedback on resume-job description compatibility.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🌟 Features

- **PDF Resume Parsing**: Extracts text from PDF resumes using `pdfminer.six`
- **Keyword Matching**: Identifies important keywords and skills from job descriptions
- **Semantic Analysis**: Uses Sentence Transformers to understand contextual similarity between resume and job description
- **ATS Score**: Provides a comprehensive match score (0-100%)
- **Missing Keywords Detection**: Highlights important keywords missing from your resume
- **Beautiful UI**: Clean and intuitive Streamlit interface
- **Docker Support**: Easy deployment with Docker containerization

## 🚀 How It Works

The application uses a two-pronged approach to analyze resumes:

1. **Keyword Match (37% weight)**: Extracts nouns and proper nouns from the job description using spaCy and checks if they appear in your resume.

2. **Semantic Similarity (63% weight)**: Uses Sentence Transformers (`all-MiniLM-L6-v2` model) to understand the contextual meaning and similarity between your resume and the job description. This goes beyond simple keyword matching to understand related concepts (e.g., "ML Engineer" and "Data Scientist").

**Final Score Formula:**
```
Final Score = (Keyword Match % × 0.37) + (Semantic Similarity × 0.63)
```

## 📋 Prerequisites

- Python 3.11 or higher
- pip package manager
- Docker (optional, for containerized deployment)

## 🛠️ Installation

### Option 1: Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd resume-checker
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   
   Open your browser and navigate to: `http://localhost:8501`

### Option 2: Docker Deployment

For detailed Docker deployment instructions, see [README_DOCKER.md](README_DOCKER.md)

**Quick Start:**
```bash
# Build the Docker image
docker build -t resume-checker .

# Run the container
docker run -p 8501:8501 resume-checker

# Access at http://localhost:8501
```

## 📦 Dependencies

- **streamlit**: Web application framework
- **pdfminer.six**: PDF text extraction
- **spacy**: Natural Language Processing for keyword extraction
- **scikit-learn**: Machine learning utilities (cosine similarity)
- **sentence-transformers**: Semantic text embeddings
- **numpy**: Numerical computing
- **en_core_web_sm**: spaCy English language model

## 📁 Project Structure

```
resume-checker/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── .dockerignore          # Docker ignore patterns
├── README.md              # This file
├── README_DOCKER.md       # Docker deployment guide
├── utils/
│   ├── __init__.py       # Package initializer
│   ├── parser.py         # PDF text extraction utilities
│   └── analyzer.py       # Resume analysis logic
└── assets/
    └── style.css         # Custom CSS styling
```

## 💻 Usage

1. **Upload Resume**: Click on the file uploader and select your PDF resume
2. **Paste Job Description**: Copy and paste the job description text into the text area
3. **Analyze**: Click the "Analyze Resume" button
4. **Review Results**: 
   - View your ATS match score
   - Check keyword match percentage
   - Review semantic similarity score
   - Identify missing keywords to improve your resume

## 🔍 Understanding the Results

### ATS Match Score
A percentage (0-100%) indicating how well your resume matches the job description. Higher scores indicate better alignment.

- **90-100%**: Excellent match
- **75-89%**: Good match
- **60-74%**: Fair match
- **Below 60%**: Needs improvement

### Keyword Match Score
Percentage of important keywords from the job description that appear in your resume.

### Semantic Similarity Score
AI-powered contextual similarity between your resume and the job description. This captures meaning beyond exact keyword matches.

### Missing Keywords
A list of important terms from the job description that don't appear in your resume. Consider adding these (where truthful) to improve your ATS score.

## 🎨 Customization

### Modifying the Scoring Algorithm

Edit `utils/analyzer.py` to adjust the weights:

```python
# Current weights: Keyword (37%), Semantic (63%)
final_score = (match_percentage * 0.37) + (semantic_similarity * 0.63)

# Example: Equal weights
final_score = (match_percentage * 0.50) + (semantic_similarity * 0.50)
```

### Styling

Modify `assets/style.css` to customize the UI appearance.

## 🐛 Troubleshooting

### Common Issues

**Issue**: `OSError: [E050] Can't find model 'en_core_web_sm'`

**Solution**: The spaCy model will be downloaded automatically on first run. If this fails, manually install:
```bash
python -m spacy download en_core_web_sm
```

**Issue**: PDF text extraction fails

**Solution**: Ensure your PDF contains selectable text (not scanned images). For scanned PDFs, consider using OCR preprocessing.

**Issue**: Docker build takes too long

**Solution**: The first build downloads large ML libraries (PyTorch, Transformers). This is normal and only happens once. Subsequent builds use cached layers.

## 🔒 Privacy & Security

- **No Data Storage**: Your resume and job description are processed in-memory only
- **No External API Calls**: All processing happens locally
- **Session-Based**: Data is cleared when you close the browser

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **spaCy**: For powerful NLP capabilities
- **Sentence Transformers**: For semantic text understanding
- **Streamlit**: For the amazing web framework
- **pdfminer.six**: For reliable PDF parsing

## 📧 Support

If you encounter any issues or have questions, please open an issue on GitHub.

## 🔮 Future Enhancements

- [ ] Support for DOCX resume format
- [ ] Multi-language support
- [ ] Resume improvement suggestions
- [ ] Batch processing for multiple resumes
- [ ] Export detailed analysis reports
- [ ] Integration with job boards APIs
- [ ] Resume template recommendations

---

**Made with ❤️ for job seekers everywhere**
