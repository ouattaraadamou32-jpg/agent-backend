from flask import Flask, jsonify

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
