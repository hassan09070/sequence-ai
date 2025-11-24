#!/bin/bash
# Quick Start Script for Sequence Game Full Stack

echo "🎮 Starting Sequence Game Full Stack Application..."
echo ""

# Check if backend is running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ Backend is already running on port 8000"
else
    echo "🚀 Starting backend server..."
    cd "$(dirname "$0")/backend"
    bash start.sh > backend.log 2>&1 &
    BACKEND_PID=$!
    echo "Backend PID: $BACKEND_PID"
    sleep 3
    
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
        echo "✅ Backend started successfully"
    else
        echo "❌ Failed to start backend. Check backend/backend.log"
        exit 1
    fi
fi

echo ""

# Check if frontend is running
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ Frontend is already running on port 3000"
else
    echo "🚀 Starting frontend server..."
    cd "$(dirname "$0")/frontend"
    npm run dev > frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo "Frontend PID: $FRONTEND_PID"
    sleep 5
    
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
        echo "✅ Frontend started successfully"
    else
        echo "❌ Failed to start frontend. Check frontend/frontend.log"
        exit 1
    fi
fi

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║   Sequence Game is ready!                  ║"
echo "╚════════════════════════════════════════════╝"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "To stop the servers:"
echo "  lsof -ti:8000 | xargs kill -9"
echo "  lsof -ti:3000 | xargs kill -9"
echo ""
echo "Opening browser..."
sleep 2
open http://localhost:3000 2>/dev/null || xdg-open http://localhost:3000 2>/dev/null || echo "Please open http://localhost:3000 in your browser"
