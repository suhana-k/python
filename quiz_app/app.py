from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "quiz_secret"

questions = [
    {
        "q": "What is the output of print(type(10))?",
        "options": {"A": "<class 'int'>", "B": "<class 'float'>", "C": "<class 'str'>", "D": "<class 'bool'>"},
        "ans": "A"
    },
    {
        "q": "Which keyword is used to define a function in Python?",
        "options": {"A": "function", "B": "def", "C": "fun", "D": "define"},
        "ans": "B"
    },
    {
        "q": "What is the output of print(3 * 2)?",
        "options": {"A": "5", "B": "6", "C": "32", "D": "8"},
        "ans": "B"
    },
    {
        "q": "Which data type is used to store text?",
        "options": {"A": "int", "B": "float", "C": "str", "D": "bool"},
        "ans": "C"
    },
    {
        "q": "What is the output of print(len('Python'))?",
        "options": {"A": "5", "B": "6", "C": "7", "D": "8"},
        "ans": "B"
    },
    {
        "q": "What is the output of print(10 // 3)?",
        "options": {"A": "3.3", "B": "3", "C": "4", "D": "3.0"},
        "ans": "B"
    },
    {
        "q": "Which symbol is used for comments in Python?",
        "options": {"A": "//", "B": "#", "C": "/*", "D": "--"},
        "ans": "B"
    },
    {
        "q": "What is the output of print(2 ** 3)?",
        "options": {"A": "6", "B": "8", "C": "9", "D": "5"},
        "ans": "B"
    },
    {
        "q": "Which function is used to take input from user?",
        "options": {"A": "get()", "B": "scan()", "C": "input()", "D": "read()"},
        "ans": "C"
    },
    {
        "q": "What is the output of print(bool(0))?",
        "options": {"A": "True", "B": "False", "C": "0", "D": "None"},
        "ans": "B"
    },
    {
        "q": "Which keyword is used for loop in Python?",
        "options": {"A": "loop", "B": "for", "C": "iterate", "D": "repeat"},
        "ans": "B"
    },
    {
        "q": "What is the output of print(5 % 2)?",
        "options": {"A": "2", "B": "1", "C": "0", "D": "5"},
        "ans": "B"
    },
    {
        "q": "Which data structure is immutable?",
        "options": {"A": "list", "B": "set", "C": "dict", "D": "tuple"},
        "ans": "D"
    },
    {
        "q": "What is the output of print('Hello' + 'World')?",
        "options": {"A": "Hello World", "B": "HelloWorld", "C": "Error", "D": "Hello+World"},
        "ans": "B"
    },
    {
        "q": "Which keyword is used for conditional statements?",
        "options": {"A": "if", "B": "loop", "C": "switch", "D": "case"},
        "ans": "A"
    }
]
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/start')
def start():
    session['score'] = 0
    session['q_no'] = 0
    session['answers'] = []

    session['quiz'] = random.sample(questions, len(questions))
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=["GET", "POST"])
def quiz():
    q_no = session.get('q_no', 0)
    q_list = session.get('quiz', questions)

    if q_no >= len(q_list):
        return redirect(url_for('result'))

    current_q = q_list[q_no]

    if request.method == "POST":
        selected = request.form.get("option")

        # Handle skipped question
        if not selected:
            selected = "Not Attempted"

        answers = session.get('answers', [])

        answers.append({
            "q_no": q_no + 1,
            "question": current_q['q'],
            "selected": selected,
            "correct": current_q['ans']
        })

        session['answers'] = answers

        if selected == current_q['ans']:
            session['score'] += 1

        session['q_no'] = q_no + 1
        return redirect(url_for('quiz'))

    progress = int((q_no + 1) * 100 / len(q_list))

    return render_template(
        "quiz.html",
        q=current_q,
        q_no=q_no + 1,
        total=len(q_list),
        progress=progress
    )

@app.route('/result')
def result():
    return render_template(
        "result.html",
        score=session.get('score', 0),
        total=len(session.get('quiz', questions)),
        answers=session.get('answers', [])
    )

@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)