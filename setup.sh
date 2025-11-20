#!/bin/bash

# CitiTrack Setup Script
echo "🚀 CitiTrack Setup Script"
echo "=========================="

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}\n"

# Backend Setup
echo -e "${YELLOW}📦 Setting up Backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

source venv/bin/activate
pip install -q -r requirements.txt
echo -e "${GREEN}✅ Backend dependencies installed${NC}"

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please configure backend/.env file${NC}"
fi

cd ..

# Frontend Setup
echo -e "\n${YELLOW}📦 Setting up Frontend...${NC}"
cd frontend

if [ ! -d "node_modules" ]; then
    npm install
    echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
fi

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please configure frontend/.env file${NC}"
fi

cd ..

# Blockchain Setup
echo -e "\n${YELLOW}📦 Setting up Blockchain...${NC}"
cd blockchain

if [ ! -d "node_modules" ]; then
    npm install
    echo -e "${GREEN}✅ Blockchain dependencies installed${NC}"
fi

cd ..

echo -e "\n${GREEN}✅ Setup completed!${NC}"
echo -e "\n${YELLOW}Next Steps:${NC}"
echo "1. Configure environment variables:"
echo "   - backend/.env"
echo "   - frontend/.env"
echo ""
echo "2. Start the backend:"
echo "   cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo ""
echo "3. Start the frontend (in new terminal):"
echo "   cd frontend && npm start"
echo ""
echo "4. Deploy smart contract (optional):"
echo "   cd blockchain && npx hardhat run scripts/deploy.js --network mumbai"