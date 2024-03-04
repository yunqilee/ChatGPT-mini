from flask import Flask, render_template, request, jsonify

import os
from openai import OpenAI

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template("my-chatgpt.html")


@app.route('/generate_text', methods=["POST"])
def generate_text():
    prompt = request.form["prompt"]
    prompt = str(prompt).strip()

    if not prompt:
        return "No prompt provided"

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )
    except Exception as e:
        return "Something went wrong while accessing OpenAI API"

    return completion.choices[0].message.content


if __name__ == '__main__':
    app.run()
