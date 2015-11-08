from git_star_visualizer import app, visualizer
from threading import Thread

# Run the Flask application in a separate daemon thread
t1 = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8080})
t1.setDaemon(True)
t1.start()

# Start the visualizer
visualizer.run()
