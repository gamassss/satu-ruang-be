from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from app.schemas import MessageCreate
from app.services import create_message

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            message = MessageCreate(content=data['content'], sender=data['sender'])
            created_message = await create_message(message)
            await manager.broadcast({
                "id": str(created_message.id),
                "content": created_message.content,
                "sender": created_message.sender,
                "timestamp": str(created_message.timestamp)
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({"content": f"Client #{client_id} left the chat"})