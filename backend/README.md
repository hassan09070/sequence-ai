# Sequence Game - Backend API

FastAPI backend for the Sequence board game with AI support.

## Features

- ✅ RESTful API for game management
- ✅ WebSocket support for real-time updates
- ✅ AI player integration (4 difficulty levels)
- ✅ Multiple concurrent games support
- ✅ Full game state management
- ✅ CORS enabled for frontend integration

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configuration

Copy `.env.example` to `.env` and adjust settings:

```bash
cp .env.example .env
```

### 3. Run Server

```bash
python run.py
```

Or with uvicorn directly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Game Management

- `POST /api/v1/game/create` - Create new game
- `GET /api/v1/game/{game_id}` - Get game state
- `POST /api/v1/game/{game_id}/move` - Make a move
- `POST /api/v1/game/{game_id}/ai-move` - Get AI move
- `GET /api/v1/game/{game_id}/legal-moves` - Get legal moves
- `DELETE /api/v1/game/{game_id}` - Delete game
- `GET /api/v1/game/` - List all games

### WebSocket

- `WS /ws/game/{game_id}` - Real-time game updates

## Usage Examples

### Create a Game

```bash
curl -X POST "http://localhost:8000/api/v1/game/create" \
  -H "Content-Type: application/json" \
  -d '{
    "num_players": 2,
    "ai_config": {"2": "medium"}
  }'
```

### Make a Move

```bash
curl -X POST "http://localhost:8000/api/v1/game/{game_id}/move" \
  -H "Content-Type: application/json" \
  -d '{
    "card": "5H",
    "row": 3,
    "col": 4
  }'
```

### Get AI Move

```bash
curl -X POST "http://localhost:8000/api/v1/game/{game_id}/ai-move" \
  -H "Content-Type: application/json" \
  -d '{
    "player_id": 2,
    "difficulty": "hard"
  }'
```

## Architecture

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   ├── game.py          # Game endpoints
│   │   └── websocket.py     # WebSocket manager
│   ├── models/              # Pydantic models
│   │   ├── __init__.py
│   │   └── schemas.py       # Request/Response schemas
│   └── services/            # Business logic
│       ├── __init__.py
│       └── game_service.py  # Game management
├── requirements.txt
├── run.py
└── README.md
```

## Development

### Run Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/
```

## License

Educational use only.
