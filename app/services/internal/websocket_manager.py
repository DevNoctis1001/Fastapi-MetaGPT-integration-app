from typing import Dict

class ConnectionManager:
    def __init__(self, socket):
        self.socket = socket
        self.active_connections: Dict[str, object] = {}

    async def connect(self, sid, environ):
        self.active_connections[sid] = environ

    async def disconnect(self, sid):
        self.active_connections.pop(sid, None)
        
    async def send_personal_message(self, user_id: str, message: str,):
        sid = next((sid for sid, environ in self.active_connections.items()
                    if environ.get('ai_session_id') == user_id), None)
        if sid:
            # Emit message to the user
            await self.socket.emit('message', message, room=sid)
            
            # Pseudocode - Update AISession's message_history
            # ai_session = find AISession by user_id in the database
            # ai_session.message_history.append(message)
            # save ai_session in the database
    
    async def recieve_message(self, sid, message):
        environ = self.active_connections.get(sid)
        user_id = environ.get('ai_session_id') if environ else None

        if user_id and message:
            print(message)
            # Pseudocode - Update AISession's message_history
            # ai_session = find AISession by user_id in the database
            # ai_session.message_history.append(message)
            # save ai_session in the database
            pass
    

    async def broadcast(self, message: str):
        await self.socket.emit('message', message)