from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Resume Analyzer Running"

# New: Upload & analyze endpoint
@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["resume"]
    
    # Save file temporarily
    filepath = os.path.join("temp_resume.pdf")
    file.save(filepath)

    return jsonify({
        "message": "File received successfully"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)