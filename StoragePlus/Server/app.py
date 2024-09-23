import time
from flask import Flask
from flask_cors import CORS
from models import db, OAuth2Client
from oauth2 import config_oauth
from routes import bp


def setup_app(app):
    db.init_app(app)
    config_oauth(app)
    app.register_blueprint(bp, url_prefix='')

    with app.app_context():
        db.create_all()

        # register clients
        client_base = OAuth2Client(
            client_id = 'storageplus_base',
            client_id_issued_at = int(time.time())
        )
        client_premium = OAuth2Client(
            client_id = 'storageplus_premium',
            client_id_issued_at = int(time.time())
        )
        client_deluxe = OAuth2Client(
            client_id = 'storageplus_deluxe',
            client_id_issued_at = int(time.time())
        )

        client_base_metadata = {
            "client_name": "storageplus_base",
            "client_uri": "https://universalbox:4444",
            "grant_types": ['authorization_code'],
            "redirect_uris": ['https://universalbox:4444/callback'],
            "response_types": ['code'],
            "scope": "download",
            "token_endpoint_auth_method": "client_secret_post"
        }

        client_premium_metadata = {
            "client_name": "storageplus_premium",
            "client_uri": "https://universalbox:4444",
            "grant_types": ['authorization_code'],
            "redirect_uris": ['https://universalbox:4444/callback'],
            "response_types": ['code'],
            "scope": "download upload",
            "token_endpoint_auth_method": "client_secret_post"
        }

        client_deluxe_metadata = {
            "client_name": "storageplus_deluxe",
            "client_uri": "https://universalbox:4444",
            "grant_types": ['authorization_code'],
            "redirect_uris": ['https://universalbox:4444/callback'],
            "response_types": ['code'],
            "scope": "download upload delete",
            "token_endpoint_auth_method": "client_secret_post"
        }


        client_base.set_client_metadata(client_base_metadata)
        client_premium.set_client_metadata(client_premium_metadata)
        client_deluxe.set_client_metadata(client_deluxe_metadata)

        client_base.client_secret = "base"
        client_premium.client_secret = "premium"
        client_deluxe.client_secret = "deluxe"

        db.session.add(client_base)
        db.session.add(client_premium)
        db.session.add(client_deluxe)

        db.session.commit()


def create_app(config=None):
    app = Flask(__name__)
    CORS(app)

    # load app specified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)

    setup_app(app)
    return app


app = create_app({
    'SECRET_KEY': 'secret',
    'OAUTH2_REFRESH_TOKEN_GENERATOR': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///db.sqlite',
})

if __name__ == "__main__":
    app.run(host='storageplus', ssl_context=('cert.pem', 'key.pem'), debug=True, port=3333)
