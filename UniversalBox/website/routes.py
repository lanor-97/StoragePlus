from hashlib import sha3_512
from flask import Blueprint, request, session, url_for
from flask import render_template, redirect, send_file
from .models import db, User, Oauth2Token
from .oauth import oauth
from authlib.common.encoding import json_dumps, json_loads
import requests

bp = Blueprint('routes', 'home')


# utility function returning oauth client
def get_client(plan):
    if plan == 'base':
        return oauth.storageplus_base
    elif plan == 'premium':
        return oauth.storageplus_premium
    elif plan == 'deluxe':
        return oauth.storageplus_deluxe

    return oauth.storageplus_base

# utility function returning current user (db model)


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None

# home page is user is authenticated, login page else


@bp.route('/')
def main():
    user = current_user()
    if not user:
        return redirect(url_for('routes.login'))

    r = requests.get("https://storageplus:3333/list-files", verify=False)

    filelist = []
    for file in r.text.split(','):
        filelist.append(file)

    return render_template('index.html', filelist=filelist, user=user)


# login route, if user exists -> login, else -> registration
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')

    username = request.form.get('username')
    password = sha3_512(request.form.get('password').encode()).hexdigest()
    user = User.query.filter_by(username=username).first()

    # if user exists, then username exists too, it's a login attempt
    if (user):
        user = User.query.filter_by(
            username=username, password=password).first()
        if (not user):
            return 'invalid login'

    # else it's a registration process
    else:
        user = User(username=username, password=password, plan='base')
        db.session.add(user)
        db.session.commit()

    session['id'] = user.id
    return redirect('/')


# upgrade plan route
@bp.route('/upgrade-plan', methods=['GET'])
def upgrade_plan():
    user = current_user()
    if user:
        if user.plan == 'base':
            user.plan = 'premium'
        elif user.plan == 'premium':
            user.plan = 'deluxe'

        db.session.commit()

    return redirect('/')



# authorization endpoint
@bp.route('/authorize', methods=['POST'])
def authorize():
    user = current_user()
    if user:
        return get_client(user.plan).authorize_redirect(verify=False)


# app receives authorization code and exchanges it for access code
@bp.route('/callback', methods=['GET', 'POST'])
def callback():
    user = current_user()
    if user:
        client = get_client(user.plan)
        token = client.authorize_access_token(verify=False)

        # memorize access token in db
        db.session.add(Oauth2Token(token=json_dumps(token),
                       user_id=user.id, client_id=client.client_id))
        db.session.commit()

    return redirect('/')

# download function using access token


@bp.route('/download/<filename>', methods=['GET', 'POST'])
def download(filename):
    user = current_user()
    if user:
        client = get_client(user.plan)
        db_token = Oauth2Token.query.filter_by(
            user_id=user.id, client_id=client.client_id).first()
        if db_token:
            token = json_loads(db_token.token)
            client.token = token
            resp = client.get('api/download/' + filename, verify=False)
            if resp.status_code != 200:
                return resp.text
            
            with open('/tmp/' + filename, 'wb') as f:
                f.write(resp.content)
            return send_file('/tmp/' + filename)
        return authorize()

# upload function using access token


@bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'no file'

    filename = request.files['file'].filename
    user = current_user()
    if user:
        client = get_client(user.plan)
        db_token = Oauth2Token.query.filter_by(
            user_id=user.id, client_id=client.client_id).first()
        if db_token:
            token = json_loads(db_token.token)
            client.token = token
            resp = client.post('api/upload/' + filename, files=request.files, verify=False)
            if resp.status_code != 200:
                return resp.text
            if resp.text == 'Y':
                return redirect('/')
        return authorize()

# delete function using access token


@bp.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    user = current_user()
    if user:
        client = get_client(user.plan)
        db_token = Oauth2Token.query.filter_by(
            user_id=current_user().id, client_id=client.client_id).first()
        if db_token:
            token = json_loads(db_token.token)
            client.token = token
            resp = client.post('api/delete/' + filename, verify=False)
            if resp.status_code != 200:
                return resp.text
            if resp.text == 'Y':
                return redirect('/')
        return authorize()

# user logout


@bp.route('/logout')
def logout():
    del session['id']
    return redirect('/')
