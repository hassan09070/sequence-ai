"""
WebSocket manager for real-time game updates
"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json


class ConnectionManager:
    """Manages WebSocket connections for game rooms"""
    
    def __init__(self):
        # game_id -> list of websocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, game_id: str):
        """Connect a client to a game room"""
        await websocket.accept()
        
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
        
        self.active_connections[game_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, game_id: str):
        """Disconnect a client from a game room"""
        if game_id in self.active_connections:
            if websocket in self.active_connections[game_id]:
                self.active_connections[game_id].remove(websocket)
            
            # Clean up empty game rooms
            if not self.active_connections[game_id]:
                del self.active_connections[game_id]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific client"""
        await websocket.send_json(message)
    
    async def broadcast(self, message: dict, game_id: str):
        """Broadcast a message to all clients in a game room"""
        if game_id in self.active_connections:
            disconnected = []
            
            for connection in self.active_connections[game_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.append(connection)
            
            # Remove disconnected clients
            for connection in disconnected:
                self.disconnect(connection, game_id)
    
    def get_connections_count(self, game_id: str) -> int:
        """Get number of connected clients for a game"""
        return len(self.active_connections.get(game_id, []))


# Global connection manager
manager = ConnectionManager()
