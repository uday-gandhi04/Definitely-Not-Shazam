import os
from flask import Flask, request, jsonify
from search import SearchSong

app = Flask(__name__)

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
        match_title, metadata = SearchSong(filename)

        if metadata:
            response = {
                "match": match_title,
                "title": metadata["title"],
                "artist": metadata["artist"],
                "youtube_url": metadata["youtube_url"]
            }
        else:
            response = {"match": None}

    finally:
        # Always delete temp file (success or error)
        if os.path.exists(filename):
            os.remove(filename)

    return jsonify(response)
