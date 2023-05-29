import os

import openai
from flask import Flask, render_template, request
from tenacity import retry, stop_after_attempt, wait_random_exponential

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

models = {
    "text-davinci": "text-davinci-003",
    "gpt-3.5": "gpt-3.5-turbo"
}
conversation = []
temperature = 0.5


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        conversation.append(request.form["user_dialog"])
        response = ""
        try:
            response = get_openai_chat(request.form["user_dialog"])
        except:
            response = "Chat bot is coming for you! Please try again later!"
        conversation.append(response)
        return render_template("index.html", conversation=conversation)

    return render_template("index.html", conversation=conversation)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_openai_chat(user_dialog):
    openai.Model.list()
    response = openai.Completion.create(
        model=models["text-davinci"],
        prompt=user_dialog,
        temperature=temperature
    )
    print(response.choices)
    return response.choices[0].text