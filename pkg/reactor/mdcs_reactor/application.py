from flask import Flask


application = Flask('mdcs_reactor', instance_relative_config=True)

@application.route('/')
def index():
    return 'MDCS Reactor HTTP API'
