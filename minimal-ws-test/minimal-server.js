const http = require('http');
const WebSocket = require('ws');

const server = http.createServer();
const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
    console.log('WebSocket connection established');
    ws.on('message', (message) => {
        console.log('Received:', message);
        ws.send(`Echo: ${message}`);
    });
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log(`WebSocket server is running on ws://localhost:${PORT}`);
});


// Run the server with Node.js : node minimal-server.js