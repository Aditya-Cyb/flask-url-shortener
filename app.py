from flask import Flask, request, jsonify, redirect
import string
import random

app = Flask(__name__)

# In-memory storage: {short_code: original_url}
url_map = {}

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/')
def home():
    return jsonify({"message": "Welcome User to my project Url Shortener"}), 200

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({"error": "Please provide a 'url' field"}), 400
    
    original_url = data['url']
    short_code = generate_short_code()
    
    while short_code in url_map:
        short_code = generate_short_code()
    
    url_map[short_code] = original_url
    
    return jsonify({
        "original_url": original_url,
        "short_code": short_code,
        "short_url": f"/{short_code}"
    }), 201

@app.route('/<short_code>')
def redirect_to_url(short_code):
    if short_code not in url_map:
        return jsonify({"error": "Short URL not found"}), 404
    
    original_url = url_map[short_code]
    return redirect(original_url)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)