#!/bin/bash

# Sequence Game - Full Stack Startup Script
# This script starts both backend and frontend servers

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  Sequence Game - Full Stack Launcher${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down servers...${NC}"
    kill 0  # Kill all background jobs
    exit 0
}

trap cleanup SIGINT SIGTERM

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    exit 1
fi

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python 3 found: $(python3 --version)"
echo -e "${GREEN}✓${NC} Node.js found: $(node --version)"
echo -e "${GREEN}✓${NC} npm found: $(npm --version)"
echo ""

# Backend Setup
echo -e "${BLUE}[1/4] Setting up Backend...${NC}"
cd "$BACKEND_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    pip install -q -r requirements.txt
    echo -e "${GREEN}✓${NC} Backend dependencies installed"
else
    echo -e "${RED}Warning: requirements.txt not found${NC}"
fi

echo ""

# Frontend Setup
echo -e "${BLUE}[2/4] Setting up Frontend...${NC}"
cd "$FRONTEND_DIR"

# Install Node dependencies if needed
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing Node.js dependencies (this may take a minute)...${NC}"
    npm install
    echo -e "${GREEN}✓${NC} Frontend dependencies installed"
else
    echo -e "${GREEN}✓${NC} Frontend dependencies already installed"
fi

echo ""

# Start Backend Server
echo -e "${BLUE}[3/4] Starting Backend Server...${NC}"
cd "$BACKEND_DIR"

# Start backend in background
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/sequence-backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
echo -e "${YELLOW}Waiting for backend to start...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Backend server is running on http://localhost:8000"
        echo -e "${GREEN}✓${NC} API Documentation: http://localhost:8000/docs"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}Error: Backend failed to start${NC}"
        echo -e "${YELLOW}Check logs: tail -f /tmp/sequence-backend.log${NC}"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
    sleep 1
done

echo ""

# Start Frontend Server
echo -e "${BLUE}[4/4] Starting Frontend Server...${NC}"
cd "$FRONTEND_DIR"

# Start frontend in background
npm run dev > /tmp/sequence-frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for frontend to start
echo -e "${YELLOW}Waiting for frontend to start...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Frontend server is running on http://localhost:3000"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}Error: Frontend failed to start${NC}"
        echo -e "${YELLOW}Check logs: tail -f /tmp/sequence-frontend.log${NC}"
        kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
        exit 1
    fi
    sleep 1
done

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  🎮 Sequence Game is Ready!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "${BLUE}Frontend:${NC}     http://localhost:3000"
echo -e "${BLUE}Backend API:${NC}  http://localhost:8000"
echo -e "${BLUE}API Docs:${NC}     http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"
echo ""
echo -e "${BLUE}Logs:${NC}"
echo -e "  Backend:  tail -f /tmp/sequence-backend.log"
echo -e "  Frontend: tail -f /tmp/sequence-frontend.log"
echo ""

# Keep script running and show combined logs
tail -f /tmp/sequence-backend.log /tmp/sequence-frontend.log &

# Wait for background processes
wait
