# 🏛️ CitiTrack - AI-Powered Municipal Service Delivery Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2-61DAFB.svg)](https://reactjs.org)
[![Solidity](https://img.shields.io/badge/Solidity-0.8-363636.svg)](https://soliditylang.org)

> **Empowering South African communities through AI automation, blockchain transparency, and offline-capable technology.**

CitiTrack is a hackathon project that addresses persistent municipal service-delivery challenges across South Africa by combining artificial intelligence, blockchain technology, and progressive web application design.

---

## 🎯 Problem Statement

South Africa faces critical municipal service-delivery challenges:

- 💧 Water leaks and sewage spills
- ⚡ Electricity outages
- 🚮 Waste collection delays
- 🛣️ Broken infrastructure (potholes, damaged roads)
- 📱 Unstructured reporting (WhatsApp, call centers, emails)
- 👁️ Lack of transparency and accountability
- 🏢 Low municipal capacity to process complaints

**Result**: Service-delivery protests, community frustration, and eroded trust in government institutions.

---

## ✨ Solution Overview

CitiTrack transforms municipal service delivery through three core innovations:

### 1. 🤖 AI Automation
- **Automatic Classification**: AI agent analyzes reports and categorizes issues
- **Severity Scoring**: Intelligent prioritization (Critical → High → Medium → Low)
- **Action Recommendations**: Generated workflows for municipal teams
- **Multilingual Support**: isiZulu, Sesotho, Afrikaans, and English

### 2. ⛓️ Blockchain Transparency
- **Immutable Audit Trail**: Every report event anchored on blockchain
- **Public Verification**: Anyone can verify municipal response times
- **Tamper-Proof Records**: Municipality cannot alter or delete reports
- **Trust Building**: Transparent accountability for all stakeholders

### 3. 📱 Offline-Capable PWA
- **Works Without Internet**: Report issues even in low-connectivity areas
- **Auto-Sync**: Queued reports automatically submit when online
- **Mobile-First Design**: Optimized for smartphones and feature phones
- **Low Data Usage**: Efficient for communities with limited data

---

## 🌍 Impact & SDG Alignment

CitiTrack directly addresses three UN Sustainable Development Goals:

| SDG | Impact |
|-----|--------|
| **SDG 16** - Peace, Justice & Strong Institutions | Creates accountable, transparent municipal governance |
| **SDG 11** - Sustainable Cities & Communities | Improves urban infrastructure management and community safety |
| **SDG 6** - Clean Water & Sanitation | Accelerates response to water and sanitation issues |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RESIDENT INTERFACE                        │
│  PWA (React + Tailwind) - Offline-Capable, Multilingual     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTPS/REST API
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND SERVICE LAYER                       │
│  FastAPI + Python - Microservice Architecture                │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  AI Agent    │  │  Blockchain  │  │  SMS/Notify  │     │
│  │  LangChain   │  │  Web3.py     │  │  Africa's    │     │
│  │  + LLM       │  │              │  │  Talking     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ↓                         ↓
┌──────────────┐          ┌──────────────┐
│  PostgreSQL  │          │  Blockchain  │
│  Database    │          │  Smart       │
│              │          │  Contract    │
└──────────────┘          └──────────────┘
                          (Polygon/Ethereum)
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 15+**
- **Git**

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/cititrack.git
cd cititrack
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:** `http://localhost:8000`

### 3. Frontend Setup

```bash
# Navigate to frontend (in new terminal)
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Start development server
npm start
```

**Frontend will be available at:** `http://localhost:3000`

### 4. Blockchain Setup (Optional)

```bash
# Navigate to blockchain
cd blockchain

# Install dependencies
npm install

# Compile contracts
npx hardhat compile

# Deploy to Mumbai testnet
npx hardhat run scripts/deploy.js --network mumbai
```

---

## 📋 API Endpoints

### Reports

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/reports` | Create new report |
| `GET` | `/api/reports` | List all reports (with filters) |
| `GET` | `/api/reports/{id}` | Get specific report |
| `PATCH` | `/api/reports/{id}` | Update report status |
| `POST` | `/api/reports/{id}/resolve` | Mark report as resolved |

### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/dashboard/stats` | Get aggregated statistics |

### Blockchain

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/blockchain/verify/{id}` | Verify blockchain trail |

**Full API Documentation:** Visit `http://localhost:8000/docs` after starting the backend.

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Integration Tests

```bash
# Start both backend and frontend
# Then run E2E tests
npm run test:e2e
```

---

## 🌐 Deployment

### Frontend (Netlify)

```bash
cd frontend
npm run build
netlify deploy --prod
```

**Environment Variables:**
- `REACT_APP_API_URL`: Your backend URL

### Backend (Render)

1. Connect GitHub repository to Render
2. Set environment variables in Render dashboard
3. Deploy from `backend/` directory
4. Use: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Environment Variables Required:**
```env
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
ETHEREUM_RPC_URL=https://...
AT_API_KEY=...  # Africa's Talking
```

### Database (Render PostgreSQL)

1. Create PostgreSQL instance on Render
2. Copy internal connection string
3. Add to backend environment variables

### Blockchain (Polygon Mumbai)

```bash
cd blockchain
npx hardhat run scripts/deploy.js --network mumbai
# Save contract address to backend .env
```

---

## 🔧 Configuration

### Backend Configuration (`backend/.env`)

```env
# API
API_HOST=0.0.0.0
API_PORT=8000

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/cititrack

# AI Models
OPENAI_API_KEY=sk-...
AI_MODEL=gpt-4

# Blockchain
ETHEREUM_RPC_URL=https://polygon-mumbai.g.alchemy.com/v2/...
CONTRACT_ADDRESS=0x...
PRIVATE_KEY=...

# SMS (Africa's Talking)
AT_USERNAME=sandbox
AT_API_KEY=...
AT_SENDER_ID=CitiTrack

# Storage
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
S3_BUCKET_NAME=cititrack-uploads
```

### Frontend Configuration (`frontend/.env`)

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENABLE_OFFLINE=true
REACT_APP_MAPBOX_TOKEN=...  # Optional for maps
```

---

## 📊 Features Breakdown

### For Residents

✅ Report issues via text or photo  
✅ Works offline - reports auto-sync  
✅ Track report status in real-time  
✅ Receive SMS notifications  
✅ View public transparency dashboard  
✅ Multilingual interface  
✅ Verify blockchain trail  

### For Municipal Officers

✅ Centralized issue dashboard  
✅ AI-recommended action plans  
✅ Priority-based queue  
✅ Status tracking workflow  
✅ Performance analytics  
✅ Immutable audit trail  

### For Communities

✅ Public transparency dashboard  
✅ Compare municipal performance  
✅ Historical data access  
✅ Blockchain verification  
✅ Evidence-based advocacy  

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, Tailwind CSS, PWA |
| **Backend** | FastAPI, Python 3.11 |
| **AI** | LangChain, OpenAI GPT-4, Anthropic Claude |
| **Blockchain** | Solidity, Hardhat, Polygon |
| **Database** | PostgreSQL 15 |
| **Storage** | AWS S3 |
| **SMS** | Africa's Talking |
| **Maps** | Mapbox/OpenStreetMap |
| **Hosting** | Netlify (Frontend), Render (Backend) |

---

## 🗺️ Roadmap

### Phase 1 - MVP (2 Days - Hackathon) ✅
- [x] Basic report submission
- [x] AI classification
- [x] Blockchain anchoring
- [x] Offline capability
- [x] Public dashboard

### Phase 2 - Enhancement (Month 1)
- [ ] WhatsApp integration
- [ ] Advanced geolocation
- [ ] Photo AI analysis
- [ ] Multi-municipality support
- [ ] Officer mobile app

### Phase 3 - Scale (Month 2-3)
- [ ] IoT sensor integration (water meters, etc.)
- [ ] Predictive maintenance AI
- [ ] National benchmarking
- [ ] Budget allocation tools
- [ ] Community voting features

### Phase 4 - Enterprise (Month 4+)
- [ ] Government API integration
- [ ] Inter-municipal coordination
- [ ] Advanced analytics & ML
- [ ] White-label solution
- [ ] International expansion

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

- **Your Name** - Full Stack Development
- **Team Member 2** - AI/ML Engineering
- **Team Member 3** - Blockchain Development

---

## 🙏 Acknowledgments

- **Anthropic** - 
- **OpenAI** - For GPT-4 integration
- **Africa's Talking** - For SMS infrastructure
- **Polygon** - For blockchain infrastructure
- **South African Municipalities** - For problem validation

---

## 📞 Support

- **Email**: support@cititrack.co.za
- **Twitter**: [@CitiTrackZA](https://twitter.com/CitiTrackZA)
- **Slack**: [Join our community](https://cititrack.slack.com)

---

## 🌟 Star Us!

If you find this project helpful, please give it a ⭐ on GitHub!

---

**Built with ❤️ for South Africa 🇿🇦**

*Empowering Communities Through Transparency*