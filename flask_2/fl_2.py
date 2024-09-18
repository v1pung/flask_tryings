import os
import sqlite3
from flask import Flask, render_template, request, g, flash
from FDatabase import FDatabase

# cfg
DATABASE = '/tmp/flask_2.db'
DEBUG = True
SECRET_KEY = 'sdfdsfdsfsdfsdfsdfsd1231dfsf'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(DATABASE=os.path.join(app.root_path, 'flask_2.db'))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    # connect if not already
    if not hasattr(g, 'link.db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link.db'):
        g.link_db.close()


@app.route("/")
def index():
    db = get_db()
    dbase = FDatabase(db)
    return render_template('index.html', menu=dbase.getMenu())

@app.route("/add_post", methods=["POST", "GET"])
def add_post():
    db = get_db()
    dbase = FDatabase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category = 'error')
            else:
                flash('Статья добавлена успешно', category = 'success')
        else:
            flash('Ошибка добавления статьи', category = 'error')

    return render_template('add_post.html', menu=dbase.getMenu(), title='Добавление статьи')


if __name__ == '__main__':
    app.run(debug=True)
