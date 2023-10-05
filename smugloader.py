import requests
from requests_oauthlib import OAuth1Session, OAuth1

class Connection():
    def __init__(self, API_KEY, API_SECRET):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.ACCES_TOKEN = "wGWG6kNphfqM2wW8zpZf6H7f2PzSB9Lj"
        self.ACCES_TOKEN_SECRET = "dtHhBGQK6MrQrPcL2SHHdbR73Sv7nm2bzJgFvsFj3dbrQPxvtqZsSJbgStn7jQtZ"

        # !only run when ACCES token and secret stop working!
        # self._get_acces() 

    def _get_acces(self): 
        """Gets the acces token & secret from smugmug"""
        # Define SmugMug API endpoints
        REQUEST_TOKEN_URL = 'https://api.smugmug.com/services/oauth/1.0a/getRequestToken'
        AUTHORIZE_URL = 'https://api.smugmug.com/services/oauth/1.0a/authorize'
        ACCESS_TOKEN_URL = 'https://api.smugmug.com/services/oauth/1.0a/getAccessToken'
        OAUTH_CALLBACK = 'oob'  # non-web application

        # Create an OAuth1Session with your API credentials and the callback parameter
        oauth = OAuth1Session(self.API_KEY, client_secret=self.API_SECRET, callback_uri=OAUTH_CALLBACK)

        # Get a request token and token secret
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
        print(self.ACCES_TOKEN)


class Loader(Connection):
    '''Loads pictures from smugmug, uses access token that Connection can fetch'''
    def __init__(self, API_KEY, API_SECRET):
        super().__init__(API_KEY, API_SECRET)
        self.url = 'https://api.smugmug.com/api/v2/album'

    def download(self):
        auth = OAuth1(
            self.API_KEY,
            client_secret=self.API_SECRET,
            resource_owner_key=self.ACCES_TOKEN,
            resource_owner_secret=self.ACCES_TOKEN_SECRET
        )

        response = requests.get(self.url, auth=auth)
        print(response.status_code)


