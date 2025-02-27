from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_wtf.csrf import CSRFProtect
from config import Config

app = Flask(__name__)

# db configuration
app.config.from_object(Config)

# setup cors and crsf
# csrf = CSRFProtect(app)
cors = CORS(app, origins='*')
app.config['CORS_HEADERS'] = 'Content-Type'

# initialize db
db = SQLAlchemy(app)

# import models
from models import Audio, Transcription

# register blueprints (API routes)
from routes import health, transcribe
app.register_blueprint(health.health_routes)
app.register_blueprint(transcribe.transcribe_routes)
