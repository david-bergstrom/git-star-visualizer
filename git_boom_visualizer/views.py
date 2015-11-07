from git_boom_visualizer import app, visualizer

import sys

from flask import session, redirect, url_for, escape, request, render_template

################################################################################
# Nothing
################################################################################

@app.route('/', methods=['GET', 'POST'])
def login():
    try:
        visualizer.post()
    except:
        print sys.exc_info()[0]
        print "ERROR#################################################"

    if request.method == 'POST':
        return 'ok'
    else:
        return 'david was here'


################################################################################
# Debugging features, TODO: Don't forget these if deploying
################################################################################
@app.route('/reset')
def reset():
    return 'Deleted the entire database'
