import os

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    url_for)

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)
