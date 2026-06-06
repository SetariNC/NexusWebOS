const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8080;
const HOST = '192.168.1.115'; // Ton adresse IP locale

const server = http.createServer((req, res) => {
    if (req.url === '/') {
        fs.readFile(path.join(__dirname, 'index.html'), (err, content) => {
            if (err) {
                res.writeHead(500);
                res.end('Erreur serveur');
            } else {
                res.writeHead(200, { 'Content-Type': 'text/html' });
                res.end(content);
            }
        });
    } else {
        // Pour gérer les autres requêtes (facultatif)
        res.writeHead(404);
        res.end('Page non trouvée');
    }
});

server.listen(PORT, HOST, () => {
    console.log(`🚀 Panel accessible sur le réseau à l'adresse : http://${HOST}:${PORT}`);
});