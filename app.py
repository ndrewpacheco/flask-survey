from flask import Flask, redirect, render_template, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey
app = Flask(__name__)

# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = 'secretkey'

toolbar = DebugToolbarExtension(app)

# deactivates redirect intercepts
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route("/")
def show_index():
    """shows first page of app"""
    session['responses'] = []
    title = satisfaction_survey.title
    return render_template('index.html', title=title)


@app.route("/questions/<int:id>", methods=["POST"])
def post_session(id):

    question = satisfaction_survey.questions[id]
    return render_template('questions.html', question=question)


@app.route("/questions/<int:id>")
def show_question(id):
    """shows question"""

    questions_length = len(satisfaction_survey.questions)
    responses_length = len(session['responses'])

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


@app.route("/answer", methods=["POST"])
def post_answer():
    responses = session['responses']
    responses.append(request.form["answer"])
    session['responses'] = responses

    return redirect(f"/questions/{len(responses)}")
