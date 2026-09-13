import os
from flask import Flask, jsonify, request
from google import genai

app = Flask(__name__)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/", methods=["GET"])
def accueil():
    return jsonify({
        "message": "Backend de mon agent",
        "status": "en ligne"
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    })

@app.route("/ask", methods=["GET"])
def ask():
    message = request.args.get("message", "")

    if not message:
        return jsonify({
            "error": "Le paramètre message est obligatoire"
        }), 400

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=message
        )

        return jsonify({
            "response": response.text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
