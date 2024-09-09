import os
import sqlite3

from flask import Flask

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


if __name__ == '__main__':
    app.run(debug=True)
