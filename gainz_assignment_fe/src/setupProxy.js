// src/setupProxy.js
const { createProxyMiddleware } = require("http-proxy-middleware");

console.log("Proxy middleware is active"); // Add this line

module.exports = function (app) {
	// Proxy API requests
	app.use(
		"/api",
		createProxyMiddleware({
			target: "http://localhost:8000",
			changeOrigin: true,
		})
	);

	// Proxy WebSocket connections
	app.use(
		"/ws",
		createProxyMiddleware({
			target: "ws://localhost:8000",
			changeOrigin: true,
			ws: true,
			logLevel: "debug", // Optional: helpful for debugging
		})
	);
};
