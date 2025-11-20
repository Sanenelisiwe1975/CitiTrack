# CitiTrack Backend

FastAPI backend for CitiTrack platform.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
app/
├── main.py              # FastAPI application
├── config.py            # Configuration
├── models/              # Pydantic models
├── api/                 # API routes
├── services/            # Business logic
├── db/                  # Database layer
└── utils/               # Utilities
```