from flask import Flask, render_template, url_for, request, flash, session, redirect, abort

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fgddgffd7gdg76df5gdg7d'
menu = [{"name": "Home", "url": "/"},
        {"name": "About", "url": "/about"},
        {"name": "Profile", "url": "/profile/aaa"},
        {"name": "Contact", "url": "/contact"},
        {"name": "Login", "url": "/login"}]


@app.route("/index")
@app.route("/")
def index():
    # print(url_for('index'))
    return render_template('index.html', menu=menu)


@app.route("/about.html")
@app.route("/about")
def about():
    print(url_for('about'))
    return render_template('about.html', title="about smth", menu=menu)


@app.errorhandler(404)
def pageNotFound():
    return render_template('page404.html', title='Page not found', menu=menu), 404


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == "POST" and request.form['username'] == 'aaa' and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title='Authentification', menu=menu)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        print(request.form)
        if len(request.form['username']) > 2:
            flash('Message submitted', category='success')
        else:
            flash('Error. Length of username must be greater than 2', category='error')

    return render_template('contact.html', title="contact", menu=menu)


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return render_template('profile.html', title=f"{username} profile", menu=menu)


with app.test_request_context():
    print(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
