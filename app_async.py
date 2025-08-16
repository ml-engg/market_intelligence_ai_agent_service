from flask import Flask, request, jsonify
# Assuming agent.py now exposes an async function
from agent import run_agent_task  
import asyncio
import datetime
import json
import aiofiles  # For asynchronous file I/O
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)

LOG_FILE = "c:/personal/agent_and_rag_market_comparison_service/log/agent_results.log"

async def log_result_async(prompt: str, result: str):
    """Log prompt and result to file with timestamp asynchronously."""
    timestamp = datetime.datetime.utcnow().isoformat()
    entry = {
        "timestamp": timestamp,
        "prompt": prompt,
        "result": result
    }
    log_line = json.dumps(entry, ensure_ascii=False)

    # Use aiofiles for asynchronous file writing
    async with aiofiles.open(LOG_FILE, mode="a", encoding="utf-8") as f:
        await f.write(log_line + "\n")


@app.route("/analyze", methods=["POST"])
async def analyze():
    """
    POST endpoint to run market analysis using the agent asynchronously.
    Expects JSON:
    {
        "prompt": "Compare Brand_a with Brand_b shampoo"
    }
    """
    try:
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "Missing 'prompt' in request body"}), 400

        user_prompt = data["prompt"]
        
        # Await the asynchronous agent task
        result = await run_agent_task(user_prompt) 
        
        # Log the interaction asynchronously
        await log_result_async(user_prompt, result)

        return jsonify({"result": result})

    except Exception as e:
        # In a real application, you'd want more specific error logging
        print(f"Error in /analyze: {e}") 
        return jsonify({"error": str(e)}), 500

asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
