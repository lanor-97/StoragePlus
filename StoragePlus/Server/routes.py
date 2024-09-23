import os
from flask import Blueprint, request, session
from flask import render_template, redirect, jsonify, send_from_directory, make_response
from authlib.integrations.flask_oauth2 import current_token
from authlib.oauth2 import OAuth2Error
from models import db, User
from oauth2 import authorization, require_oauth
from hashlib import sha3_512
from werkzeug.utils import secure_filename


bp = Blueprint('routes', __name__)

# utility function returning user model


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None

# CLI Application related functions

# login function from cli application


@bp.route('/app-login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = sha3_512(request.form.get('password').encode()).hexdigest()
    user = User.query.filter_by(
        username=username, password=password).first()

    if (user):
        session['id'] = user.id
        print(session['id'])
        return 'Y'
    return 'N'

# register function from cli application


@bp.route('/app-register', methods=['POST'])
def register():
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()

    if (not user):
        password = sha3_512(request.form.get('password').encode()).hexdigest()
        new_user = User(
            username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['id'] = new_user.id
        return 'Y'
    return 'N'

# list files function from cli application


@bp.route('/list-files', methods=['GET'])
def list_files():
    #username = request.form.get('username')
    #hashed_password = sha3_512(request.form.get('password').encode()).hexdigest()

    # return db.register_newuser(username, hashed_password)
    files = ""
    for file_ in os.listdir(os.getcwd() + "/userfiles/"):
        files += file_ + ","

    if files:
        return files[:-1]
    else:
        return "N"

# download file function from cli application


@bp.route('/userfiles/<path:filename>', methods=['GET'])
def download_file(filename):
    files_dir = os.path.join(os.getcwd(), 'userfiles')
    return send_from_directory(files_dir, filename)

# upload file function from cli application


@bp.route('/upload/<filename>', methods=['POST'])
def upload_file(filename):
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file:
        filename = secure_filename(filename)
        file.save(os.path.join(os.getcwd() + "/userfiles/", filename))
        return 'Y'
    else:
        return 'N'

# delete file function from cli application


@bp.route('/delete/<path:filename>', methods=['POST'])
def delete_file(filename):
    try:
        os.remove(os.path.join(os.getcwd() + "/userfiles/", filename))
        return 'Y'
    except FileNotFoundError:
        return 'N'

# logout function from cli application


@bp.route('/logout')
def logout():
    if id in session:
        del session['id']
    return ''


# oauth auth methods

# oauth login, used only for successive authorization
@bp.route('/oauth/login', methods=['GET', 'POST'])
def oauth_login():
    if request.method == 'POST':
        username = request.form.get('username')
        hashed_password = sha3_512(
            request.form.get('password').encode()).hexdigest()
        user = User.query.filter_by(
            username=username, password=hashed_password).first()
        if not user:
            return "Invalid login"
        session['id'] = user.id

        # if user is not just to log in, but need to head back to the auth page, then go for it
        next_page = request.form.get('next')
        if next_page:
            return redirect(next_page)
        return redirect('/')

    user = current_user()

    return render_template('login.html', user=user)

# oauth authorization, creating an auth code and calling the client callback uri


@bp.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    user = current_user()

    # if user log status is not true (Auth server), then to log it in
    if not user:
        return render_template('login.html', next=request.url)
    if request.method == 'GET':
        try:
            grant = authorization.get_consent_grant(end_user=user)
        except OAuth2Error as error:
            return error.error
        return render_template('authorize.html', user=user, grant=grant)

    if not user and 'username' in request.form:
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
    if request.form['confirm']:
        grant_user = user
    else:
        grant_user = None

    return authorization.create_authorization_response(grant_user=grant_user)

# creating oauth access token


@bp.route('/oauth/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()

# oauth revoke


@bp.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_endpoint_response('revocation')


# oauth API section

# download function api with access token
@bp.route('/api/download/<filename>', methods=['GET'])
@require_oauth(['download'])
def api_download(filename):
    user = current_token.user
    if not user:
        return make_response(jsonify(error="user not found"), 404)

    return download_file(filename)  # TODO

# upload function api with access token


@bp.route('/api/upload/<filename>', methods=['POST'])
@require_oauth(['upload'])
def api_upload(filename):
    user = current_token.user
    if not user:
        return make_response(jsonify(error="user not found"), 404)

    return upload_file(filename)    # TODO

# delete function api with access token


@bp.route('/api/delete/<filename>', methods=['POST'])
@require_oauth(['delete'])
def api_delete(filename):
    user = current_token.user
    if not user:
        return make_response(jsonify(error="user not found"), 404)

    return delete_file(filename)    # TODO
