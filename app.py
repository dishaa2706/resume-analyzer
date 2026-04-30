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

# -----------------------------
# PDF TEXT EXTRACTION FUNCTION
# -----------------------------
def extract_text_from_pdf(filepath):
    text = ""
    with open(filepath, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text

# -----------------------------
# SKILL LIST
# -----------------------------
skills_list = [
    "python", "java", "c++", "sql", "html", "css", "javascript",
    "linux", "windows", "aws", "azure", "docker", "kubernetes",
    "machine learning", "data analysis", "excel", "git"
]

# -----------------------------
# SKILL EXTRACTION FUNCTION
# -----------------------------
def extract_skills(text):
    found_skills = []
    text = text.lower()

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills

# -----------------------------
# ANALYZE ROUTE
# -----------------------------
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

    if not text.strip():
        return jsonify({"error": "Could not extract text from PDF"})

    # Extract skills
    skills = extract_skills(text)

    # Simple scoring
    score = len(skills) * 10

    return jsonify({
        "text_preview": text[:300],
        "skills": skills,
        "score": score
    })

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)