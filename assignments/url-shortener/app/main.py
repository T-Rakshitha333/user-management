# main.py
from flask import Flask, request, jsonify, redirect
from utils import generate_short_code, is_valid_url
from models import store

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    long_url = data['url']
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL format"}), 400

    # Generate a new unique short code
    short_code = generate_short_code()
    while store.get_url(short_code):
        short_code = generate_short_code()

    store.add_url(short_code, long_url)
    short_url = f"{request.host_url}{short_code}"

    return jsonify({"short_code": short_code, "short_url": short_url}), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    entry = store.get_url(short_code)
    if not entry:
        return jsonify({"error": "Short URL not found"}), 404

    store.increment_clicks(short_code)
    return redirect(entry['url'], code=302)

@app.route('/api/stats/<short_code>', methods=['GET'])
def stats(short_code):
    entry = store.get_stats(short_code)
    if not entry:
        return jsonify({"error": "Short URL not found"}), 404

    return jsonify({
        "url": entry["url"],
        "clicks": entry["clicks"],
        "created_at": entry["created_at"]
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
