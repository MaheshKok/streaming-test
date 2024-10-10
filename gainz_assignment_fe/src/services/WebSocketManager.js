// src/services/WebSocketManager.js
// Not in use
class WebSocketManager {
	constructor() {
		this.webSocket = null;
	}

	setWebSocket(ws) {
		this.webSocket = ws;
	}

	sendMessage(message) {
		if (this.webSocket && this.webSocket.readyState === WebSocket.OPEN) {
			this.webSocket.send(message);
		} else {
			console.error("WebSocket is not open. Cannot send message.");
		}
	}

	closeWebSocket() {
		if (this.webSocket) {
			console.log("Closing WebSocket connection");
			this.webSocket.close();
			this.webSocket = null;
		}
	}
}

const wsManager = new WebSocketManager();
export default wsManager;
