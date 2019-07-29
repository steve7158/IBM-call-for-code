from flask import Flask
from flask import render_template, request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from flask import logging

app=Flask('__main__')
@app.route('/')
def survivor_detector():
    return render_template('index.html')

if __name__=='__main__':
    app.secret_key('secret123')
    app.run(debug=True)
