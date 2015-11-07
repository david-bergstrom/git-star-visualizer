from git_boom_visualizer import app, visualizer
from threading import Thread

t1 = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8080})
t1.setDaemon(True)
t1.start()
visualizer.run()
