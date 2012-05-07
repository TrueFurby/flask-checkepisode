from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

import friendly_time
import views
import models
import login
import logger

def run():
    app.debug=True
    app.run(host=app.config['HOST'], port=app.config['PORT'])