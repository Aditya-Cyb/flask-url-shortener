# Flask URL Shortener with CI/CD Pipeline

A URL shortening API built with Flask, containerized with Docker, and deployed automatically to AWS EC2 using a GitHub Actions CI/CD pipeline.

## 🚀 Live Demo

```
http://3.7.71.208:5000
```

> Note: This is a portfolio/demo deployment on a free-tier EC2 instance and may not be running at all times.

## 📌 Overview

This project demonstrates an automated CI/CD workflow: every push to the `main` branch triggers a pipeline that runs tests, builds a Docker image, pushes it to Docker Hub, and deploys the updated container to an AWS EC2 instance — with zero manual intervention.

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Testing:** Pytest
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Cloud:** AWS EC2 (Ubuntu)
- **Registry:** Docker Hub

## 🔄 CI/CD Pipeline

```
Code Push → GitHub Actions Triggered
              │
              ▼
        ┌─────────┐
        │  Test   │  → Run pytest suite
        └────┬────┘
             ▼
      ┌──────────────┐
      │ Build & Push │  → Build Docker image, push to Docker Hub
      └──────┬───────┘
             ▼
        ┌─────────┐
        │ Deploy  │  → SSH into EC2, pull latest image, restart container
        └─────────┘
```

The pipeline is defined in [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml) and runs three sequential jobs:

1. **test** — Installs dependencies and runs the pytest suite. The pipeline stops here if any test fails.
2. **build-and-push** — Builds a Docker image from the `Dockerfile` and pushes it to Docker Hub.
3. **deploy** — Connects to the EC2 instance over SSH, pulls the newly pushed image, stops the old container, and starts the new one.

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| POST | `/shorten` | Create a short URL. Body: `{"url": "https://example.com"}` |
| GET | `/<short_code>` | Redirects to the original URL |
| GET | `/health` | Health check endpoint |

### Example

```bash
curl -X POST http://3.7.71.208:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

Response:
```json
{
  "original_url": "https://www.google.com",
  "short_code": "aB3xY9",
  "short_url": "/aB3xY9"
}
```

## 🖥️ Running Locally

```bash
# Clone the repo
git clone https://github.com/Aditya-Cyb/flask-url-shortener.git
cd flask-url-shortener

# Set up virtual environment
python -m venv venv
source venv/bin/activate   # or venv/Scripts/activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest test_app.py -v

# Run the app
python app.py
```

## 🐳 Running with Docker

```bash
docker build -t flask-url-shortener .
docker run -d -p 5000:5000 flask-url-shortener
```

## ⚙️ Pipeline Setup (for reference)

The pipeline relies on four GitHub repository secrets:

| Secret | Purpose |
|--------|---------|
| `DOCKERHUB_USERNAME` | Docker Hub login |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `EC2_HOST` | EC2 instance public IP |
| `EC2_SSH_KEY` | Private SSH key for deployment |

## 📈 What This Project Demonstrates

- Writing automated tests as a quality gate before deployment
- Containerizing an application with Docker
- Building a multi-stage CI/CD pipeline with GitHub Actions
- Managing secrets securely for automated deployments
- Deploying to and managing a cloud VM (AWS EC2)

## 👤 Author

**Aditya Dutta**
[LinkedIn](https://linkedin.com/in/aditya-dutta-link) · [GitHub](https://github.com/Aditya-Cyb)
