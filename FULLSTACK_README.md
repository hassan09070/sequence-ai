# 🎮 Sequence Game - Full Stack Application

A complete full-stack implementation of the classic Sequence board game featuring a **Python/FastAPI backend** with AI opponents and a **Next.js/React frontend** with beautiful UI.

## 🌟 Features

### Backend (Python/FastAPI)
- ✅ RESTful API for game management
- ✅ WebSocket support for real-time updates
- ✅ AI opponents with 4 difficulty levels (Easy, Medium, Hard, Expert)
- ✅ Minimax algorithm with Alpha-Beta pruning
- ✅ Multiple concurrent games support
- ✅ Complete game state management
- ✅ CORS enabled

### Frontend (Next.js/TypeScript)
- ✅ Beautiful, responsive game board
- ✅ Interactive card selection
- ✅ Real-time legal move highlighting
- ✅ Animated chip placement
- ✅ AI opponent integration
- ✅ Game creation wizard
- ✅ Live game status updates

## 📁 Project Structure

```
projectAI/
├── game/                    # Original Python game logic
│   ├── board.py
│   ├── deck.py
│   ├── player.py
│   └── gamestate.py
├── ai/                      # AI implementation
│   ├── heuristics.py
│   └── minimax.py
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── models/         # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt
│   └── start.sh            # Startup script
└── frontend/                # Next.js frontend
    ├── app/
    │   ├── page.tsx        # Home page
    │   └── game/[gameId]/  # Game page
    ├── components/
    │   └── game/           # Game UI components
    ├── lib/                # API client
    └── types/              # TypeScript types
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13+ (or 3.10+)
- Node.js 18+
- npm or yarn

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the server
bash start.sh
```

Backend will run on **http://localhost:8000**

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on **http://localhost:3000**

### 3. Play!

1. Open http://localhost:3000 in your browser
2. Configure your game (2-3 players, Human/AI)
3. Click "Start Game"
4. Enjoy!

## 🎯 How to Play

1. **Select a Card**: Click on a card from your hand
2. **Legal Moves Highlighted**: Valid positions light up on the board
3. **Place Chip**: Click a highlighted cell to place your chip
4. **Form Sequences**: Create 5 in a row (horizontal, vertical, or diagonal)
5. **Win**: First to complete required sequences wins!

## 🤖 AI Difficulty Levels

- **Easy**: Depth 1, basic moves
- **Medium**: Depth 2, decent strategy
- **Hard**: Depth 3, strong play
- **Expert**: Depth 4, expert level

## 📡 API Endpoints

### Game Management
- `POST /api/v1/game/create` - Create new game
- `GET /api/v1/game/{gameId}` - Get game state
- `POST /api/v1/game/{gameId}/move` - Make a move
- `POST /api/v1/game/{gameId}/ai-move` - Get AI move
- `GET /api/v1/game/{gameId}/legal-moves` - Get legal moves
- `DELETE /api/v1/game/{gameId}` - Delete game

### WebSocket
- `WS /ws/game/{gameId}` - Real-time game updates

### Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.13
- **WebSocket**: Native websockets
- **CORS**: Enabled for frontend
- **AI**: Custom Minimax with Alpha-Beta pruning

### Frontend
- **Framework**: Next.js 15
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **API Client**: Fetch API
- **Real-time**: WebSocket

## 🎨 UI Components

- **GameBoard**: 10×10 interactive grid
- **Cell**: Individual board position with card and chip
- **Card**: Playing card with suit symbols
- **PlayerHand**: Display player's cards
- **GameInfo**: Game status and player information

## 🔧 Development

### Backend Development

```bash
cd backend

# Run with auto-reload
bash start.sh

# Or manually
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend

# Development mode
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## 🌐 Environment Variables

### Backend (.env)
```bash
HOST=0.0.0.0
PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## 📊 Architecture

```
┌─────────────────┐         ┌──────────────────┐
│   Next.js       │  HTTP/  │  Python Backend  │
│   Frontend      │  WS     │  (FastAPI)       │
│                 │ ◄─────► │                  │
│  - React UI     │         │  - game/         │
│  - Game Board   │         │  - ai/           │
│  - Cards        │         │  - API routes    │
│  - Animations   │         │  - WebSocket     │
└─────────────────┘         └──────────────────┘
```

## ✨ Key Improvements Over CLI Version

1. **Visual Interface**: Beautiful, intuitive game board
2. **Real-time Updates**: Instant move feedback
3. **Better UX**: Card selection, move highlighting
4. **Responsive Design**: Works on desktop and mobile
5. **Concurrent Games**: Multiple games at once
6. **Easy Setup**: Simple configuration wizard
7. **Professional Look**: Modern, polished design

## 🎓 Learning Outcomes

This project demonstrates:
- Full-stack architecture
- REST API design
- WebSocket real-time communication
- AI algorithm implementation
- Modern React patterns
- TypeScript best practices
- Responsive UI design
- State management
- Error handling

## 📝 Future Enhancements

- [ ] User authentication
- [ ] Multiplayer over internet
- [ ] Game lobby/matchmaking
- [ ] Game history and replay
- [ ] Statistics and leaderboards
- [ ] Chat system
- [ ] Mobile app (React Native)
- [ ] Tournament mode

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -ti:8000 | xargs kill -9

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Check if port 3000 is in use
lsof -ti:3000 | xargs kill -9

# Clear cache and reinstall
rm -rf node_modules .next
npm install
```

### Can't connect frontend to backend
- Ensure backend is running on port 8000
- Check CORS settings in backend/app/config.py
- Verify API_URL in frontend .env.local

## 📄 License

Educational use only.

## 🤝 Contributing

This is an educational project. Feel free to fork and experiment!

## 🎉 Credits

- Original game logic: Python CLI version
- Backend: FastAPI + Python
- Frontend: Next.js + React + Tailwind CSS
- AI: Minimax with Alpha-Beta pruning

---

**Enjoy playing Sequence! 🎮🎯**
