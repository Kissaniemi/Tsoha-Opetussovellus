from os import getenv
from flask import Flask

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

with app.app_context():
    import debug
    debug.initSetup()
    
import routes
