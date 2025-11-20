# 🚀 CitiTrack Quick Start Guide

Get CitiTrack running in 5 minutes!

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or use Docker)

## Option 1: Automated Setup (Recommended)

```bash
# Run setup script
./setup.sh

# Configure environment variables
nano backend/.env
nano frontend/.env

# Start backend (Terminal 1)
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Start frontend (Terminal 2)
cd frontend
npm start
```

## Option 2: Docker Setup

```bash
cd deployment/docker
docker-compose up --build
```

Access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Option 3: Manual Setup

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with backend URL
npm start
```

### Database

```bash
# Using PostgreSQL
createdb cititrack

# Update DATABASE_URL in backend/.env
DATABASE_URL=postgresql://user:password@localhost:5432/cititrack
```

## Configuration

### Required Environment Variables

**Backend (.env):**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/cititrack
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=sk-...  # Optional for AI features
```

**Frontend (.env):**
```env
REACT_APP_API_URL=http://localhost:8000
```

### Optional Services

#### OpenAI (AI Classification)
1. Get API key from https://platform.openai.com
2. Add to backend/.env: `OPENAI_API_KEY=sk-...`

#### AWS S3 (Photo Storage)
1. Create S3 bucket
2. Add credentials to backend/.env

#### Africa's Talking (SMS)
1. Register at https://africastalking.com
2. Add credentials to backend/.env

#### Blockchain (Polygon Mumbai)
1. Get RPC URL from https://alchemy.com
2. Deploy contract: `cd blockchain && npx hardhat run scripts/deploy.js --network mumbai`
3. Add contract address to backend/.env

## Testing

### Test Backend
```bash
cd backend
pytest tests/
```

### Test Frontend
```bash
cd frontend
npm test
```

### Test Smart Contract
```bash
cd blockchain
npx hardhat test
```

## Troubleshooting

### Backend won't start
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Ensure all dependencies installed: `pip install -r requirements.txt`

### Frontend won't start
- Check Node.js version: `node --version` (should be 18+)
- Clear cache: `rm -rf node_modules package-lock.json && npm install`

### Database connection error
- Ensure PostgreSQL is running
- Check connection string format
- Create database if it doesn't exist

## Next Steps

1. **Explore the Application**
   - Submit a test report
   - View dashboard
   - Check API documentation at /docs

2. **Deploy to Production**
   - Follow [DEPLOYMENT.md](docs/DEPLOYMENT.md)
   - Configure production environment variables
   - Set up monitoring

3. **Customize**
   - Modify categories in backend/app/models/report.py
   - Update translations in frontend/src/utils/translations.js
   - Customize UI in frontend/src/components/

## Support

- Documentation: See `docs/` folder
- Issues: Create GitHub issue
- API Reference: http://localhost:8000/docs

---

**Happy coding! 🎉**v o