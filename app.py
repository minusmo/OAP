import os

import openai
from flask import Flask, redirect, render_template, request, url_for
from tenacity import retry, stop_after_attempt, wait_random_exponential

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

model = "text-davinci-003"
conversation = []
temperature = 0.3


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        response = get_openai_chat(request.form["user_dialog"])
        conversation.append(response.choices[0].text)
        return redirect(url_for("index", result=response.choices[0].text, conversation=conversation))

    result = request.args.get("result")
    return render_template("index.html", result=result)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_openai_chat(user_dialog):
    response = openai.Completion.create(
        model=model,
        prompt=user_dialog,
        temperature=temperature
    )
    return response
def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )
