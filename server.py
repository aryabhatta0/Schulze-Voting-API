from flask import Flask, request, jsonify
from flask_cors import CORS
from schulze import run_schulze

# Flask sets up the server and handles requests
app = Flask(__name__)
CORS(app)  # Enabling CORS

@app.route("/getResult", methods=["POST"])
def get_result():
    try:
        data = request.json
        candidates = data["candidates"]
        ballots = data["ballots"]
        outcome = run_schulze(len(candidates), ballots, candidates)
        # Extract only the candidate indexes from the outcome
        outcome = [group["indexes"] for group in outcome]
        return jsonify(outcome)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Schulze Voting API!"

if __name__ == "__main__":
    app.run(port=5000)
