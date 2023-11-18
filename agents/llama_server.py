import os
import time

import torch
import transformers
from transformers import GenerationConfig
from flask import Flask, request, jsonify

DEFAULT_SYSTEM_PROMPT = """You are a helpful, respectful and honest assistant."""






generation_config = GenerationConfig(**{
    "bos_token_id": 1,
    "do_sample": False,
    "eos_token_id": 2,
    "max_new_tokens": 800,
    "pad_token_id": 0,
    "transformers_version": "4.32.1"
})


def run_inference(prompt):
    sequences = pipeline(
        get_prompt_chat(prompt),
        generation_config=generation_config
    )
    completion = sequences[0]["generated_text"]
    return completion


# This ensures the model is loaded only once when the server starts
model_name = "meta-llama/Llama-2-70b-chat-hf"
tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
model = transformers.AutoModelForCausalLM.from_pretrained(model_name,
                                                          trust_remote_code=True,
                                                          load_in_8bit=True)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device_map="auto",
)

# Flask app initialization
app = Flask(__name__)


# Flask route for inference
@app.route('/inference', methods=['POST'])
def inference():
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = run_inference(message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# [Your existing run_inference and other related functions]

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)