from git_boom_visualizer import app, visualizer


@app.route('/', methods=['GET', 'POST'])
def login():
    visualizer.post()
    return ''
