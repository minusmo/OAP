import os
import uuid
import openai
from flask import Flask, render_template, request, session
from tenacity import retry, stop_after_attempt, wait_random_exponential

app = Flask(__name__)
app.config.update(SECRET_KEY=str(uuid.uuid4()), SESSION_TYPE="chat_id")
openai.api_key = os.getenv("OPENAI_API_KEY")

models = {
    "text-davinci": "text-davinci-003",
    "gpt-3.5": "gpt-3.5-turbo"
}

temperature = 0.7

@app.route("/", methods=("GET", "POST"))
def index():
    conversation = session.get('conversation', None)
    if not conversation:
        session['conversation'] = []
    if request.method == "POST":
        session['conversation'].append(request.form["user_dialog"])
        openai_response = ""
        try:
            openai_response = get_openai_chat(request.form["user_dialog"])
        except:
            openai_response = "Chat bot is coming for you! Please try again later!"
        session['conversation'].append(openai_response)
        return render_template("index.html", conversation=session['conversation'])

    return render_template("index.html", conversation=session['conversation'])

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

if __name__ == "__main__":
    app.run(host="0.0.0.0")