import os
import sqlite3

from flask import Flask, render_template, request, g, flash, abort, make_response

from FDatabase import FDatabase

app = Flask(__name__)

menu = [{"title": "Главная", "url": "/"},
        {"title": "Добавить статью", "url": "/add_post"}]

@app.route("/")
def index():
    return "<h1>Main page</h1>"

@app.route("/login")
def login():
    log = ""
    if request.cookies.get('logged'):
        log = request.cookies.get('logged')

    res = make_response(f"<h1>Форма авторизации</h1><p>logged: {log}")
    res.set_cookie("logged", "yes")
    return res

if __name__ == '__main__':
    app.run(debug=True)
