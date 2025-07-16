from flask import Flask, request, jsonify
from flask_cors import CORS
from search import SearchSong 
import os

app = Flask(__name__)
CORS(app)     # Enable CORS for all routes

@app.route("/api/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save temporarily
    filename = "temp_input.mp3"
    file.save(filename)

    try:
        # Perform search
        metadata = SearchSong(filename)

        if metadata:
            response = [{
                "title": song["title"],
                "artist": song["artist"],
                "youtube_url": song["youtube_url"],
                "confidence": song["confidence"]
            } for song in metadata]
        else:
            response = {"match": None}

    finally:
        # Always delete temp file (success or error)
        if os.path.exists(filename):
            os.remove(filename)

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
