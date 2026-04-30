from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import PyPDF2

app = Flask(__name__)
CORS(app)

# Home route
@app.route("/")
def home():
    return "Resume Analyzer Running"

# Function to extract text from PDF
def extract_text_from_pdf(filepath):
    text = ""
    with open(filepath, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text

# Analyze route
@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["resume"]

    # Save file
    filepath = "temp_resume.pdf"
    file.save(filepath)

    # Extract text
    text = extract_text_from_pdf(filepath)

    # Handle empty text
    if not text.strip():
        return jsonify({
            "error": "Could not extract text from PDF"
        })

    return jsonify({
        "text_preview": text[:500]
    })

# Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)