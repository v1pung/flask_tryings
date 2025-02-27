from datetime import datetime

from flask import Flask, render_template, request, g, current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.now)

    pr = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f"<users {self.id}>"


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profiles {self.id}"


@app.route("/")
def index():
    info = []
    try:
        info = Users.query.all()
    except Exception as e:
        print("ошибка чтения из бд " + str(e))
    return render_template('index.html', title="Главная", list = info)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        # validation
        # ...
        try:
            hashed = generate_password_hash(request.form['psw'])
            u = Users(email=request.form['email'], psw=hashed)
            db.session.add(u)
            db.session.flush()

            p = Profiles(name=request.form['name'], old=request.form['old'],
                         city=request.form['city'], user_id=u.id)
            db.session.add(p)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Ошибка добавления записи в БД " + str(e))

    return render_template('register.html', title="Регистрация")


if __name__ == "__main__":
    app.run(debug=True)
    with app.app_context():
        db.create_all()
