from flask import Flask, request, jsonify
from flask_cors import CORS
from search import SearchSong 
from downloader import download_youtube_url
from index import index_new_songs
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



@app.route("/api/contribute", methods=["POST"])
def contribute():
    data = request.get_json()
    url = data.get("url")

    url=url.split("&")[0] # Remove any additional parameters from the URL
    if not url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    try:
        print(f"Downloading from URL: {url}")
        download_youtube_url(url)
        print("Download complete, indexing new songs...")
        index_new_songs()
        return jsonify({"status": "success", "message": "Thanks for your contribution!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
