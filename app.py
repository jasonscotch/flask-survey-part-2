from flask import Flask, render_template, request, redirect, flash, session
from surveys import satisfaction_survey


from flask_debugtoolbar import DebugToolbarExtension



app = Flask(__name__)
app.config['SECRET_KEY'] = 'password123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


# responses = []

@app.route('/')
def index():
    """Returns homepage"""
    return render_template('home.html', title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)

@app.route('/start', methods=['POST'])
def start():
    """Clearing saved session responses"""
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<int:question_number>', methods=['POST', 'GET'])
def question_page(question_number):
    """Displays the current question and collects the user's response. Also makes sure users stay in order on the questions and cant skip ahead."""
    responses = session.get('responses')
    if question_number != len(responses):
        flash('You are accessing an invalid question. Redirecting back to your survey.')
        return redirect(f'/questions/{len(responses)}')
    
    if request.method == 'POST':
        selected_choice = request.form['choice']
        responses = session['responses']
        responses.append(selected_choice)
        session['responses'] = responses
        # Redirect to the next question or to the survey completion page if this is the last question
        if question_number == len(satisfaction_survey.questions) - 1:
            return redirect('/thanks')
        else:
            next_question_number = question_number + 1
            return redirect(f'/questions/{next_question_number}')
    else:
        return render_template('question.html', question=satisfaction_survey.questions[question_number].question, choices=satisfaction_survey.questions[question_number].choices, question_number=question_number )


@app.route('/thanks')
def thanks():
    """Displays the completion page with a message thanking the user for completing the survey"""
    questions = satisfaction_survey.questions
    responses = session.get('responses')
    zip_responses = zip(questions, responses)
    
    print(len(responses), len(questions)) 
    return render_template('thanks.html', zip_responses=zip_responses, questions=questions)

# @app.route('/responses')
# def responses():
#     """Saves the responses in a session"""
    
#     redirect('/questions/')