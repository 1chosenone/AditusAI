# 🚪 _Aditus AI_
  > *Aditus* — Latin for "access", "entrance", or "opportunity"
> 
A personal career intelligence platform that monitors job opportunities, industry trends, and learning resources, and delivers tailored insights to help you grow and land the right role.

---

## 🗺️ Overview

Navigating the job market as a new graduate is overwhelming. _Aditus_ AI acts as a **career co-pilot** that continuously works in the background to surface what matters: the right jobs, the right skills, and the right learning resources, all tailored to your profile.

The platform ingests your resume, builds a structured candidate profile, and then runs automated workflows to match you with opportunities and tell you what to learn next.

## 👥 Target Audience

The initial version targets **recent software engineering graduates** who, like me, struggle to identify the most relevant job opportunities and skills to develop. I started building AditusAI to help myself navigate this challenge, and the platform also aims to support others in the same situation.

⚠️ The long-term goal is to generalize the platform to support job seekers across any domain or specialization.

## ✨ Features

The app currently focuses on four core workflows to streamline career growth and professional development.

### 1. 📄 Resume Ingestion
Upload a PDF resume and transform it into a structured candidate profile, including skills, interests, and experience—using OCR and LLM-based extraction.

### 2. 🔍 Job Discovery
Automatically scrape, analyze, and rank relevant job postings based on the candidate profile, including match scoring and skill gap analysis.

### 3. 📡 Tech Radar
Monitor industry trends and emerging technologies relevant to the user's skills and target roles.

### 4. 📚 Learning Digest
Turn market trends into personalized, actionable learning recommendations, highlighting skills most in demand.

### 📦 Technologies

**Backend**
- `Python` : main programming language for backend logic and data processing.
- `FastAPI` : backend framework for building APIs.

**Orchestration**
- `n8n` : workflow automation for orchestrating data pipelines and repetitive tasks.
- `Redis Queue (RQ)` : simple Python library for background task processing using Redis as a queue.

**Databases**
- `SQLite` : lightweight relational database for storage of structured data (CVs, jobs, skills).
- `MongoDB` : document database for storing unstructured text like job descriptions, learning digest, and articles.
- `Qdrant` : vector database for advanced semantic search and matching based on embeddings.

**AI / LLM**
- `litellm` : unified interface for 100+ LLM providers, letting developers choose and switch their preferred model via a consistent API.
- `instructor` : structured output library built on top of LiteLLM that enforces Pydantic schema validation on LLM responses, with automatic retries on malformed outputs.
- LLM APIs (OpenAI / Anthropic) : used for resume parsing


## Architecture
> 🚧 This section will be updated as the project progresses.

## 🚦Running the project

### Prerequisites
- Redis must be running: `docker run -p 6379:6379 redis`
- Copy `.env.example` to `.env` and configure required variables

### 1. Install dependencies
```bash
uv sync
```

### 2. Start FastAPI server
```bash
uv run fastapi dev main.py
```

### 3. Start Redis worker (in a separate terminal)
```bash
uv run rq worker default
```


## 📚 What I learned
> 🚧 This section will be completed upon project completion
