from visualizer import Visualizer
from flask import Flask

visualizer = Visualizer()
app = Flask(__name__)

import views
