# Docker Deployment Guide

## 1. Build the Docker Image
Run the following command in the terminal to build the image. This might take a few minutes as it needs to download large ML libraries (Torch, Spacy models).

```bash
docker build -t resume-checker .
```

## 2. Run the Container
Once built, run the container mapping port 8501:

```bash
docker run -p 8501:8501 resume-checker
```

## 3. Access the App
Open your browser and go to:
http://localhost:8501
