# AI Social Post Creator

An AI-powered social media post generator with React frontend and FastAPI backend.

## Features

- Generate social media posts optimized for Twitter, Instagram, LinkedIn, Facebook
- Choose tone, count, and topic/brief for posts
- Export generated posts as CSV
- Clean, user-friendly UI with TailwindCSS
- Backend powered by OpenAI API (GPT-4o-mini)
- Dockerized with easy Docker Compose setup
- Continuous Integration with GitHub Actions for backend tests and frontend linting
- Ready for deployment on popular platforms

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional for containerized run)
- OpenAI API key (for full AI generation)

### Local Dev

Backend:

```bash
cd backend
pip install -r requirements.txt
export OPENAI_API_KEY="your_openai_api_key_here"
uvicorn backend:app --reload --port 8000
