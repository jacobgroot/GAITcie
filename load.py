'''This file loads all images from SmugMug'''
from requests_oauthlib import OAuth1Session


# Define your API key and API secret
api_key = 'vgDq8WpPDCKdWTM8F9bX5d6HdT8mRRvD'
api_secret = 'XVXkQGKsFpJk9tHbMJHZdZgTBNbLrgCjW3f3XL4hQLFLbjHJq6QvLc64h82Zzp2d'

# Set the API endpoint to list albums
url = 'https://api.smugmug.com/api/v2/album'

# Create an OAuth1Session 
oauth = OAuth1Session(api_key, client_secret=api_secret, signature_type='query') # search documentation if we really need "query"

# Make the authenticated GET request
response = (oauth.get(
        url,
        headers={'Accept': 'application/json'}).text)
print(response)
if response.status_code == 200:
    print("succes")
else:
    print(f"Request failed with status code: {response.status_code}")
