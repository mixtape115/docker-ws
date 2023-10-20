# docker-ws

## main.py
```
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods={"*"},
    allow_headers=["*"]
)

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
```
WebSocket通信を扱うためにFastAPIで提供されるWebSocketエンドポイントやConnectionManagerを導入する主なメリットは次のとおりです：

 - アーキテクチャの整理: FastAPIのWebSocketエンドポイントとConnectionManagerを使用することで、WebSocket通信のアーキテクチャがより整理されます。WebSocket接続の受け入れ、切断、メッセージの送信、ブロードキャストなどの一般的な操作を効率的に処理できます。

 - 再利用性: ConnectionManagerクラスやWebSocketエンドポイントの導入により、WebSocket関連のコードを再利用できます。このようなコードの再利用は、将来的にWebSocket通信を他の部分で使用する場合に役立ちます。

 - 保守性と拡張性: FastAPIのWebSocketツールを使用することで、コードがより保守可能になり、新しい機能を追加しやすくなります。WebSocket通信のルールや振る舞いは明示的になり、理解しやすくなります。

 - エラーハンドリング: WebSocket通信はエラーが発生する可能性が高いため、ConnectionManagerを使用するとエラーハンドリングを強化できます。WebSocketエンドポイントは切断された接続をきちんと処理できます。

 - セキュリティ: ConnectionManagerを使用して、WebSocket接続を制御し、アクセスを制限できます。また、CORSの設定により、信頼されたオリジンからのみWebSocket接続を許可することができます。

 - リアルタイム通信: ConnectionManagerとWebSocketエンドポイントの導入により、リアルタイムの双方向通信を実現できます。これは、リアルタイムチャット、ライブデータ更新、ゲーム、コラボレーションツールなど多くのアプリケーションで有用です。

したがって、FastAPIのWebSocketツールを導入することで、WebSocket通信をより効率的かつセキュアに扱え、アプリケーションの拡張性と保守性を向上させることができます。



```
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods={"*"},
    allow_headers=["*"]
)
```
FastAPIアプリケーションでWebSocket通信を処理するための設定とクラス
どのオリジンからでもリクエストを受け付ける
allow_origins、allow_credentials、allow_methods、およびallow_headersはCORSポリシーの設定を指定


```
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
```
WebSocket接続を管理するためのユーティリティクラス
WebSocket接続をリストで追跡し、新しい接続を受け入れ、既存の接続を切断し、メッセージを送信したり、全ての接続にブロードキャストしたりする