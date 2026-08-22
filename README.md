# Flask URL Shortener — CI/CD Pipeline & Auto-Scaling Infrastructure

A URL shortening API built with Flask, containerized with Docker, and deployed through two progressively more advanced AWS setups:

1. **[CI/CD Pipeline](#-1-cicd-pipeline)** — automated test → build → deploy to a single EC2 instance
2. **[Auto-Scaling Web App](#-2-auto-scaling-web-app)** — a highly available, self-healing deployment behind a Load Balancer and Auto Scaling Group

## 🚀 Live Demos

| Deployment | URL |
|---|---|
| CI/CD (single instance) | `http://3.7.71.208:5000` |
| Auto-Scaling (load balanced) | `http://load-balancer-alb-769084583.ap-south-1.elb.amazonaws.com` |

> Note: These are portfolio/demo deployments on free-tier AWS resources and may not be running at all times.

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Testing:** Pytest
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Cloud:** AWS (EC2, Application Load Balancer, Auto Scaling, AMI)
- **Registry:** Docker Hub

---

## 📦 1. CI/CD Pipeline

Every push to `main` triggers a pipeline that tests, builds, and deploys the app automatically — with zero manual intervention.

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

Defined in [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml), the pipeline runs three sequential jobs:

1. **test** — Installs dependencies and runs the pytest suite; stops here if any test fails.
2. **build-and-push** — Builds a Docker image and pushes it to Docker Hub.
3. **deploy** — SSHes into EC2, pulls the new image, stops the old container, and starts the new one.

---

## ⚖️ 2. Auto-Scaling Web App

Extends the same app into a highly available architecture: multiple EC2 instances behind a Load Balancer, with instances launched or terminated automatically based on demand.

```
                         ┌─────────────────────────┐
   Internet  ──────────▶ │  Application Load        │
                         │  Balancer (ALB)           │
                         └────────────┬──────────────┘
                                      │
                              ┌───────▼────────┐
                              │  Target Group   │
                              │  (HTTP:5000,    │
                              │  /health check)  │
                              └───────┬────────┘
                                      │
                     ┌────────────────┼────────────────┐
                     ▼                ▼                ▼
              ┌────────────┐   ┌────────────┐   ┌────────────┐
              │  EC2        │   │  EC2        │   │  EC2        │
              │  Instance   │   │  Instance   │   │  Instance   │
              └────────────┘   └────────────┘   └────────────┘
                     ▲                ▲                ▲
                     └────────────────┴────────────────┘
                        Auto Scaling Group
                     (min 1, desired 2, max 4)
                     scales on CPU utilization
```

### Components

| Component | Purpose |
|---|---|
| **AMI** | Custom image built from a working EC2 instance with Docker and the app pre-installed |
| **Launch Template** | Defines new instance configuration, plus a user-data script that auto-starts the Docker container on boot |
| **Target Group** | Routes traffic to registered instances on port 5000, using `/health` for health checks |
| **Application Load Balancer** | Public entry point; distributes traffic across healthy instances |
| **Auto Scaling Group** | Maintains desired instance count, replaces unhealthy instances, scales on CPU utilization (target: 50%) |

### Bootstrap script (user data)

```bash
#!/bin/bash
docker start flask-app || docker run -d -p 5000:5000 --name flask-app --restart=always adityadev02/flask-url-shortener:latest
```

### 🐛 Real-World Issues Solved

- **`InvalidParameterCombination` — instance type not Free Tier eligible:** The Auto Scaling Group had an instance-type override active, ignoring the Launch Template. Fixed by resetting the ASG to use the Launch Template directly.
- **vCPU service limit reached:** Other running instances hit the account's vCPU quota, blocking new launches. Resolved by stopping unused instances.
- **Instances failing health checks:** New instances booted correctly, but the Docker container didn't start automatically. Fixed with a user-data bootstrap script and an Instance Refresh rollout.

---

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
git clone https://github.com/Aditya-Cyb/flask-url-shortener.git
cd flask-url-shortener

python -m venv venv
source venv/bin/activate   # or venv/Scripts/activate on Windows

pip install -r requirements.txt
pytest test_app.py -v
python app.py
```

## 🐳 Running with Docker

```bash
docker build -t flask-url-shortener .
docker run -d -p 5000:5000 flask-url-shortener
```

## 📈 What This Project Demonstrates

- Writing automated tests as a quality gate before deployment
- Containerizing an application with Docker
- Building a multi-stage CI/CD pipeline with GitHub Actions
- Designing high-availability, self-healing infrastructure on AWS
- Configuring Load Balancers, Target Groups, and Auto Scaling policies
- Debugging real infrastructure issues using cloud provider logs and metrics

## 👤 Author

**Aditya Dutta**
[LinkedIn](https://linkedin.com/in/aditya-dutta-link) · [GitHub](https://github.com/Aditya-Cyb)
