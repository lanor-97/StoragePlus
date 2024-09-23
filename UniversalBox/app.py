from website.app import create_app
import warnings


warnings.filterwarnings("ignore")


app = create_app({
    'SECRET_KEY': 'secret',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///db.sqlite',
})

if __name__ == "__main__":
    app.run(host='universalbox', ssl_context=('cert.pem', 'key.pem'), debug=True, port=4444)
