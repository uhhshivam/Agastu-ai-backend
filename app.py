import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)

CORS(app, origins=[
    "https://uhhshivam.github.io"
])

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


@app.route("/")
def home():
    return "AGASTU AI Backend is running!"


@app.route("/ask", methods=["POST"])
def ask():
    if client is None:
        return jsonify({
            "error": "Gemini API key is not configured"
        }), 500

    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "error": "Please enter a question"
        }), 400

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=(
                "You are AGASTU AI, a friendly tutor for "
                "CBSE Class 11 and 12 students in India. "
                "Explain concepts step by step using simple "
                "language and examples. Help with Physics, "
                "Chemistry, Mathematics and Computer Science.\n\n"
                f"Student's question: {question}"
            )
        )

        return jsonify({
            "answer": response.text
        })

    except Exception:
        app.logger.exception("Gemini request failed")

        return jsonify({
            "error": "AI could not answer. Check the backend logs."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
