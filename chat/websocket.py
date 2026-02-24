from fastapi import WebSocket, WebSocketDisconnect
from chat.manager import manager
from sheets.messages_repo import save_message, save_group_message


async def chat_socket(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            msg_type = data.get("type")

            if msg_type == "direct":
                to = data["to"]
                message = data["message"]

                save_message(user_id, to, message)
                await manager.send_to_user(to, {
                    "from": user_id,
                    "message": message
                })

            elif msg_type == "group":
                group_id = data["group_id"]
                message = data["message"]

                save_group_message(group_id, user_id, message)
                await manager.broadcast_group(group_id, {
                    "from": user_id,
                    "message": message,
                    "group_id": group_id
                })

    except WebSocketDisconnect:
        manager.disconnect(user_id)
