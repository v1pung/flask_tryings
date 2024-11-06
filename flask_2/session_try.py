import datetime

from flask import Flask, session

app = Flask(__name__)
app.config['SECRET_KEY'] = '80c367f983bc4ecf1d28defaf0d765405cea1f30'
app.permanent_session_lifetime = datetime.timedelta(days=10)


@app.route("/")
def index():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return f"<h1>Main Page</h1><p>Число просмотров: {session['visits']}"


data = [1, 2, 3, 4]


@app.route("/session")
def session_data():
    session.permanent = True
    if 'data' not in session:
        session['data'] = data
    else:
        session['data'][1] += 1
        session.modified = True

    return f"<p>session['data']: {session['data']}"


if __name__ == '__main__':
    app.run(debug=True)
