import requests
import os
from requests_oauthlib import OAuth1Session, OAuth1

class Connection():
    def __init__(self, API_KEY, API_SECRET, ACCES_TOKEN, ACCES_TOKEN_SECRET):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.ACCES_TOKEN = ACCES_TOKEN
        self.ACCES_TOKEN_SECRET = ACCES_TOKEN_SECRET

        # !only run when ACCES token and secret stop working!
        # self._get_acces() 

    def _get_acces(self): 
        """Gets the acces token & secret from smugmug"""
        # Define SmugMug API endpoints
        REQUEST_TOKEN_URL = 'https://api.smugmug.com/services/oauth/1.0a/getRequestToken'
        AUTHORIZE_URL = 'https://api.smugmug.com/services/oauth/1.0a/authorize'
        ACCESS_TOKEN_URL = 'https://api.smugmug.com/services/oauth/1.0a/getAccessToken'
        OAUTH_CALLBACK = 'oob'  # non-web application

        # use OAuth to create session
        oauth = OAuth1Session(self.API_KEY, client_secret=self.API_SECRET, callback_uri=OAUTH_CALLBACK)

        # Get request token and token secret
        fetch_response = oauth.fetch_request_token(REQUEST_TOKEN_URL)

        # Extract request token and secret
        request_token = fetch_response.get('oauth_token')
        request_token_secret = fetch_response.get('oauth_token_secret')

        # Redirect user to the authorization URL
        authorization_url = oauth.authorization_url(AUTHORIZE_URL)
        print("Open URL and authorize application:", authorization_url)
        verifier = input("Enter the SmugMug number: ")

        # Get access token secret
        oauth = OAuth1Session(self.API_KEY, client_secret=self.API_SECRET, resource_owner_key=request_token, resource_owner_secret=request_token_secret, verifier=verifier)
        access_token_response = oauth.fetch_access_token(ACCESS_TOKEN_URL)

        # Extract access token and secret
        self.ACCES_TOKEN = access_token_response.get('oauth_token')
        self.ACCES_TOKEN_SECRET = access_token_response.get('oauth_token_secret')

class Loader(Connection):
    ''' Loads pictures from smugmug, uses access token that Connection can fetch
        Does not download videos. If you also want to download videos, turn self.__download_vid True
        If you only want to download videos, turn self.__download_img off'''
    
    def __init__(self, API_KEY, API_SECRET, ACCES_TOKEN, ACCES_TOKEN_SECRET):
        super().__init__(API_KEY, API_SECRET, ACCES_TOKEN, ACCES_TOKEN_SECRET)
        self.auth = auth = OAuth1(
            self.API_KEY,
            client_secret=self.API_SECRET,
            resource_owner_key=self.ACCES_TOKEN,
            resource_owner_secret=self.ACCES_TOKEN_SECRET
        )
        self.headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Methods': "GET"}
        self.__download_img = True
        self.__download_video = False
        self.alb_url = 'https://api.smugmug.com/api/v2/folder/user/rubenlugters!albumlist'
        self.img_base_url = 'https://api.smugmug.com/api/v2/album/' 
        self.download_directory = os.path.join(os.getcwd(), 'media')

        # i have the media path, but when Gerstenat wants to use it, they might not have it
        if not os.path.exists(self.download_directory):
            os.makedirs(self.download_directory)

        self.images = []

    def download(self):
        '''Performs downloading operation. Uses self.__download params to specify downloading type'''
        response_raw = requests.get(self.alb_url, auth=self.auth, headers=self.headers)

        if response_raw.status_code != "200":
            self._get_acces

        response = response_raw.json()
        for album in response["Response"]["AlbumList"]:
            self.__search_nested_album(album)
            print(f"downloading album: {album['Name']}...")
            
    def __search_nested_album(self, album):

        try:
            print(album)
            for _album in album["AlbumList"]:
                print(_album)
                self.__search_nested_album(_album)
        except:
            self.__retreive_img(album)
        
    def __retreive_img(self, album):            
        images_url = 'https://api.smugmug.com' + album["Uri"] + "!images"
        imgs = requests.get(images_url, auth=self.auth, headers=self.headers).json()     
        for pic in imgs["Response"]["AlbumImage"]:
            self.__download_media(pic["ArchivedUri"])           

    def __download_media(self, image_url):
        """ Downloads images and videos, on conditions of params __download
            Writes all media to download_directory"""

        image_name = image_url.split("/")[-1]  # Extract the image name from the URL
        image_path = os.path.join(self.download_directory, image_name)

        # perform download type check
        if self.__download_video and image_name[-3:] != "mp4":
            return
        if self.__download_img and image_name[-3:] != "jpg":
            return 
        
        response = requests.get(image_url, auth=self.auth)
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(response.content)
            # print(f"Downloaded: {image_name}")
        else:
            # print(response.status_code)
            # print)
            print(f"Failed to download: {image_name}")




