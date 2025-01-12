const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const os = require('os');

const app = express();
const TARGET_PORT = 3000;
const PROXY_PORT = 5000;

// Function to get the local IP address for accessing the server from the phone
function getLocalIPAddress() {
    const interfaces = os.networkInterfaces();
    for (const name in interfaces) {
        for (const iface of interfaces[name]) {
            if (iface.family === 'IPv4' && !iface.internal) {
                return iface.address;
            }
        }
    }
    return 'localhost';
}

// ✅ CORS Fix: Apply Headers for All Requests
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
    if (req.method === 'OPTIONS') {
        return res.sendStatus(200);  // Preflight response
    }
    next();
});

// ✅ Force Rewrite Absolute URL to Proxy Host IP
app.use(
    createProxyMiddleware({
        target: `http://localhost:${TARGET_PORT}`,
        changeOrigin: true,
        ws: true,
        logLevel: 'debug',

        // Rewrite absolute URLs dynamically to force the proxy usage
        onProxyReq: (proxyReq, req) => {
            proxyReq.setHeader('Origin', `http://${getLocalIPAddress()}:${PROXY_PORT}`);
        }
    })
);

// Start the Proxy Server
app.listen(PROXY_PORT, () => {
    const localIP = getLocalIPAddress();
    console.log(`Proxy server running at:`);
    console.log(`- PC Access: http://localhost:${PROXY_PORT}`);
    console.log(`- Mobile Access: http://${localIP}:${PROXY_PORT}`);
    console.log(`All requests will be forwarded to: http://localhost:${TARGET_PORT}`);
});
