from flask import Flask
from git_star_visualizer import visualizer

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    visualizer.post()
    return ''
