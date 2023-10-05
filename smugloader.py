from requests_oauthlib import OAuth1Session

class Connection():
    def __init__(self, API_KEY, API_SECRET):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.ACCES_TOKEN = None
        self.ACCES_TOKEN_SECRET = None
        self._get_acces()

    def _get_acces(self): 
        """Gets the acces token & secret from smugmug"""
        # Define SmugMug API endpoints
        REQUEST_TOKEN_URL = 'https://api.smugmug.com/services/oauth/1.0a/getRequestToken'
        AUTHORIZE_URL = 'https://api.smugmug.com/services/oauth/1.0a/authorize'
        ACCESS_TOKEN_URL = 'https://api.smugmug.com/services/oauth/1.0a/getAccessToken'
        OAUTH_CALLBACK = 'oob'  # Change this to your actual callback URL or 'oob'

        # Create an OAuth1Session with your API credentials and the callback parameter
        oauth = OAuth1Session(self.API_KEY, client_secret=self.API_SECRET, callback_uri=OAUTH_CALLBACK)

        # Step 1: Get a request token and token secret
        fetch_response = oauth.fetch_request_token(REQUEST_TOKEN_URL)

        # Extract the request token and secret
        request_token = fetch_response.get('oauth_token')
        request_token_secret = fetch_response.get('oauth_token_secret')

        # Redirect the user to the authorization URL
        authorization_url = oauth.authorization_url(AUTHORIZE_URL)
        print("Please go to the following URL and authorize the application:", authorization_url)
        verifier = input("Enter the verifier: ")

        #Get the access token and access token secret
        oauth = OAuth1Session(self.API_KEY, client_secret=self.API_SECRET, resource_owner_key=request_token, resource_owner_secret=request_token_secret, verifier=verifier)
        access_token_response = oauth.fetch_access_token(ACCESS_TOKEN_URL)

        # Extract the access token and secret
        self.ACCES_TOKEN = access_token_response.get('oauth_token')
        self.ACCES_TOKEN_SECRET = access_token_response.get('oauth_token_secret')


class Loader(Connection):
    '''Loads pictures from smugmug, uses acces token that Connection can fetch'''
    def __init__(self, API_KEY, API_SECRET):
        super().__init__(API_KEY, API_SECRET)
        self._get_acces()