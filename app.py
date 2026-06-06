from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import psutil

app = Flask(__name__)
CORS(app)

# Configuration des dossiers
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
NOTES_DIR = os.path.join(ROOT_DIR, "notes")

if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)

# --- API SYSTEM STATS ---
@app.route('/api/stats')
def get_stats():
    return jsonify({
        "cpu": psutil.cpu_percent(interval=None),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    })

# --- API EXPLORATEUR ---
@app.route('/api/files', defaults={'subpath': ''})
@app.route('/api/files/<path:subpath>')
def list_files(subpath):
    try:
        target_path = os.path.join(ROOT_DIR, subpath.replace('/', os.sep)).strip()
        if not os.path.exists(target_path):
            return jsonify({"items": [], "error": "Not found"}), 404
        items = []
        for name in os.listdir(target_path):
            full_item_path = os.path.join(target_path, name)
            items.append({
                "name": name,
                "isDir": os.path.isdir(full_item_path),
                "path": os.path.join(subpath, name).replace("\\", "/")
            })
        return jsonify({"items": items})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- API NOTES ---
@app.route('/api/notes', methods=['GET', 'POST'])
def handle_notes():
    if request.method == 'POST':
        data = request.json
        filename = data.get('filename', 'note.txt')
        if not filename.endswith('.txt'): filename += '.txt'
        content = data.get('content', '')
        with open(os.path.join(NOTES_DIR, filename), 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({"status": "saved"})
    
    files = [f for f in os.listdir(NOTES_DIR) if f.endswith('.txt')]
    return jsonify({"notes": files})

@app.route('/api/notes/<filename>')
def get_note_content(filename):
    try:
        with open(os.path.join(NOTES_DIR, filename), 'r', encoding='utf-8') as f:
            return jsonify({"content": f.read()})
    except:
        return jsonify({"error": "File not found"}), 404

# --- SERVIR L'INTERFACE ---
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    print(f"Nexus Server running on http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)