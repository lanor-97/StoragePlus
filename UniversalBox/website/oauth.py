from authlib.integrations.flask_client import OAuth

oauth = OAuth()

# client registration
oauth.register(
    name='storageplus_base',
    client_id='storageplus_base',
    client_secret='base',
    access_token_url='https://storageplus:3333/oauth/token',
    access_token_params=None,
    authorize_url='https://storageplus:3333/oauth/authorize',
    authorize_params=None,
    api_base_url='https://storageplus:3333/',
    client_kwargs={'scope': 'download', 'token_endpoint_auth_method': 'client_secret_post'}
)

oauth.register(
    name='storageplus_premium',
    client_id='storageplus_premium',
    client_secret='premium',
    access_token_url='https://storageplus:3333/oauth/token',
    access_token_params=None,
    authorize_url='https://storageplus:3333/oauth/authorize',
    authorize_params=None,
    api_base_url='https://storageplus:3333/',
    client_kwargs={'scope': 'download upload', 'token_endpoint_auth_method': 'client_secret_post'}
)

oauth.register(
    name='storageplus_deluxe',
    client_id='storageplus_deluxe',
    client_secret='deluxe',
    access_token_url='https://storageplus:3333/oauth/token',
    access_token_params=None,
    authorize_url='https://storageplus:3333/oauth/authorize',
    authorize_params=None,
    api_base_url='https://storageplus:3333/',
    client_kwargs={'scope': 'download upload delete', 'token_endpoint_auth_method': 'client_secret_post'}
)
