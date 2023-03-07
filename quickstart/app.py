import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


# @app.route("/", methods=("GET", "POST"))
# def index():
#     if request.method == "POST":
#         ft_model = 'ada:ft-personal-2023-03-06-20-50-42'
#         user_input = request.form["user_input"]
#         response = openai.Completion.create(
#             model=ft_model,
#             prompt=grab_user_input(user_input) + '\n\n###\n\n',
#             max_tokens=1,
#             temperature=0.6
#         )

#         return redirect(url_for("index", result=response.choices[0]['text']))

#     result = request.args.get("result")
#     return render_template("index.html", result=result)

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        ft_model = "gpt-3.5-turbo"
        user_input = request.form["user_input"]
        response = openai.ChatCompletion.create(
            model=ft_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "I'd like to go to Miami"},
                {"role": "assistant", "content": "Where are you flying from?"},
                {"role": "user", "content": user_input}
            ],
            # prompt=grab_user_input(user_input),
            # max_tokens=1,
            # temperature=0.6
        )

        print('output:', response['choices'][0]['message']['content'])

        # return redirect(url_for("index", result=response['choices'][0]['message']['content']))
        return render_template("index.html", result=response['choices'][0]['message']['content'])

    result = request.args.get("result")
    return render_template("index.html", result=result)

TRAINING_EXAMPLES = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "I'd like to go to Miami"},
                {"role": "assistant", "content": "Where are you flying from?"},
                {"role": "user", "content": "I gotta be in Texas next week."},
                {"role": "assistant", "content": "Which city are you flying from?"},
                {"role": "user", "content": "I have a work trip in NYC in April."},
                {"role": "assistant", "content": "Where would you like to depart from?"},
                {"role": "user", "content": "My friend is getting married in Chicago this October. Can you book me a ticket to Chicago around that time?"},
                {"role": "assistant", "content": "I'd be happy to help. Where are you flying from?"},
                {"role": "user", "content": "I need to go a funeral next week in Idaho."},
                {"role": "assistant", "content": "I'm sorry to hear that. Where are you departing from?"},]

@app.route("/api/chat")
def chat():
    req = request.json()
    ft_model = "gpt-3.5-turbo"
    user_input = req["user_input"]
    history = req['history']
    history += [{"role": "user", "content": user_input}]
    response = openai.ChatCompletion.create(
        model=ft_model,
        messages=TRAINING_EXAMPLES + history,
    )
    response_line = response['choices'][0]['message']['content']
    return {"next_line": response_line, "all_lines": history+[{"role": "assistant", "content": response_line}]}


def grab_user_input(user_input):
    return user_input + '\n\n###\n\n'
