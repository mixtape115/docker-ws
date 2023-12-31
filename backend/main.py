from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

# FastAPIアプリケーションでWebSocket通信を処理するための設定とクラス
# どのオリジンからでもリクエストを受け付ける
# allow_origins、allow_credentials、allow_methods、およびallow_headersはCORSポリシーの設定を指定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods={"*"},
    allow_headers=["*"]
)

# WebSocket接続を管理するためのユーティリティクラス
# WebSocket接続をリストで追跡し、新しい接続を受け入れ、既存の接続を切断し、メッセージを送信したり、全ての接続にブロードキャストしたりする
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()



# フロントエンドを提供するエンドポイント
# @app.get("/")
# async def get():
#     return HTMLResponse(content=open("index.html").read(), status_code=200)
@app.get("/")
def test():
    return "test"


# WebSocket通信を処理するエンドポイント
# @app.websocket("/ws_process")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")

@app.websocket("/ws_process")
async def ws_process(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client left the chat")


