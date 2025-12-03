FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Increase pip timeout and install in stages to handle large downloads
# Install PyTorch and large dependencies first with extended timeout
# RUN pip install --no-cache-dir --timeout=1000 \
#     torch \
#     sentence-transformers \
#     && pip install --no-cache-dir --timeout=1000 \
#     streamlit \
#     scikit-learn \
#     && pip install --no-cache-dir --timeout=1000 \
#     pdfminer.six \
#     spacy \
#     numpy

RUN pip install --no-cache-dir \
    torch \
    sentence-transformers \
    && pip install --no-cache-dir \
    streamlit \
    scikit-learn \
    && pip install --no-cache-dir \
    pdfminer.six \
    spacy \
    numpy


# Install spacy model
RUN pip install --no-cache-dir \
    https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl

# Copy app code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run app
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
