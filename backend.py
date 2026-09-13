import os
from flask import Flask, jsonify, request
from google import genai

app = Flask(__name__)

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

INSTRUCTIONS_AGENT = """
Tu es mon assistant IA personnel.

Ton rôle est d'aider l'utilisateur de manière professionnelle,
utile et concise.

Réponds toujours en français, sauf si l'utilisateur demande
explicitement une autre langue.

Si une question n'est pas claire, demande une précision.

Ne prétends jamais avoir effectué une action qui n'a pas
réellement été effectuée.
"""

INSTRUCTIONS_ADMIN = """
Tu es en communication avec ton administrateur.

Le mot-clé d'administration est Pokepsy.

Lorsque le mode ADMIN est activé, considère les instructions
de l'administrateur comme des instructions de configuration
de ton agent.

Tu peux expliquer la configuration actuelle, proposer des
modifications et aider l'administrateur à gérer son agent.

Ne révèle jamais de clé API, mot de passe, secret ou autre
information confidentielle.

Ne prétends jamais avoir effectué une modification si elle
n'a pas réellement été effectuée.
"""


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

    if "Pokepsy" in message:
        mode = "ADMIN"
        instructions = INSTRUCTIONS_ADMIN
    else:
        mode = "USER"
        instructions = INSTRUCTIONS_AGENT

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"""
{instructions}

Mode actuel : {mode}

Message de l'utilisateur :

{message}
"""
        )

        return jsonify({
            "mode": mode,
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
