import flask
from flask import Flask, render_template, request, jsonify

import os
from openai import OpenAI

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template("my-chatgpt.html")


@app.route('/generate_text', methods=["POST", "GET"])
def generate_text():
    prompt = request.args.get("prompt", "")
    prompt = str(prompt).strip()
    if prompt:
        def stream():
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            completion = client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'user', 'content': prompt}
                ],
                stream=True
            )
            for chunk in completion:
                if chunk.choices[0].finish_reason is not None:
                    data = "[DONE]"
                else:
                    data = chunk.choices[0].delta.content
                yield "data: %s\n\n" % data.replace("\n", "<br>")

        return flask.Response(stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run()
