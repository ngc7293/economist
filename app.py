from flask import Flask, abort
from os import path
from economist import convert

app = Flask(__name__)

@app.route('/')
def test():
    return 'Hello World!'

@app.route('/economist.css')
def css():
    return open('templates/economist.css', 'r').read()

@app.route('/<path:article>')
def get(article):
    name = article.split('/')[-1]
    filename = 'articles/{name}.html'.format(name=name)

    if path.exists(filename):
        print("Serving pre-converted article")
        return open(filename,'r').read()
    else:
        convert('http://economist.com/{article}'.format(article=article), '.html', True)
        if path.exists(filename):
            return open(filename,'r').read()

    abort(500)