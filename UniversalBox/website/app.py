from flask import Flask
from flask_cors import CORS
from .models import db
from .routes import bp
from .oauth import oauth

def create_app(config=None):
	app = Flask(__name__)
	CORS(app)

	# load app specified configuration
	if config is not None:
		if isinstance(config, dict):
			app.config.update(config)

	setup_app(app)
	return app


def setup_app(app):
	db.init_app(app)
	oauth.init_app(app)
	app.register_blueprint(bp, url_prefix='')
	
	with app.app_context():
		db.create_all()