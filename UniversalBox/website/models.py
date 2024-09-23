from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(40), unique=True)
	password = db.Column(db.String(128))
	plan = db.Column(db.String(10))

	def get_user_id(self):
		return self.id

	def check_password(self, password):
		return password == self.password

	def get_plan(self):
		return self.plan
		

class Oauth2Token(db.Model):
	__tablename__ = "oauth2_token"
	token = db.Column(db.Text, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
	client_id = db.Column(db.Text)
