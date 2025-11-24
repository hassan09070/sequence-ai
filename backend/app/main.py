"""
FastAPI Main Application
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .api import game_router
from .api.websocket import manager
from .services import game_manager

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(game_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "active_games": len(game_manager.list_games())
    }


@app.websocket("/ws/game/{game_id}")
async def websocket_game(websocket: WebSocket, game_id: str):
    """
    WebSocket endpoint for real-time game updates
    
    Clients can connect to receive real-time updates about game state changes
    """
    await manager.connect(websocket, game_id)
    
    try:
        # Send initial connection message
        await manager.send_personal_message(
            {
                "type": "connected",
                "game_id": game_id,
                "message": "Connected to game"
            },
            websocket
        )
        
        # Listen for messages
        while True:
            data = await websocket.receive_json()
            
            # Handle different message types
            message_type = data.get("type")
            
            if message_type == "move":
                # Broadcast move to all clients
                await manager.broadcast(
                    {
                        "type": "move",
                        "game_id": game_id,
                        "data": data
                    },
                    game_id
                )
            
            elif message_type == "state_update":
                # Broadcast state update
                await manager.broadcast(
                    {
                        "type": "state_update",
                        "game_id": game_id,
                        "data": data
                    },
                    game_id
                )
            
            elif message_type == "player_joined":
                # Broadcast player joined
                await manager.broadcast(
                    {
                        "type": "player_joined",
                        "game_id": game_id,
                        "data": data
                    },
                    game_id
                )
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id)
        
        # Notify other clients
        await manager.broadcast(
            {
                "type": "player_disconnected",
                "game_id": game_id,
                "connections": manager.get_connections_count(game_id)
            },
            game_id
        )
    
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket, game_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
