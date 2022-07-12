from flask import Flask, redirect, render_template, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey
app = Flask(__name__)

# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = '<replace with a secret key>'

toolbar = DebugToolbarExtension(app)

# deactivates redirect intercepts
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []

# def __init__(self, title, instructions, questions):


@app.route("/")
def show_index():
    """shows first page of app"""
    title = satisfaction_survey.title
    return render_template('index.html', title=title)


@app.route("/questions/<int:id>")
def show_question(id):
    """shows question"""

    questions_length = len(satisfaction_survey.questions)
    responses_length = len(responses)

    # if responses is full
    if responses_length == questions_length:
        return render_template('thanks.html')

    # if id mismatched with sequence of questions
    elif id != responses_length:
        flash("You're trying to access an invalid question!")
        return redirect(f"/questions/{responses_length}")
    else:
        question = satisfaction_survey.questions[responses_length]
        return render_template('questions.html', question=question)
    # else:
    #     return render_template('thanks.html')


@app.route("/answer", methods=["POST"])
def post_answer():

    responses.append(request.args)
    print(responses)
    id = len(responses)

    return redirect(f"/questions/{id}")
