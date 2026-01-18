from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from chatbot import get_agent_executor

app = Flask(__name__)
CORS(app)

# Initialize agent
agent_executor = get_agent_executor()

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        if agent_executor:
            result = agent_executor.invoke({"input": user_input})
            response = result["output"]
            return jsonify({"response": response})
        else:
            return jsonify({"error": "Agent not initialized"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
