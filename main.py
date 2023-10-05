'''Imports filtered images and calls facial recognition, than saves the files to local system.  '''
from smugloader import Loader

API_KEY = 'vgDq8WpPDCKdWTM8F9bX5d6HdT8mRRvD'
API_SECRET = 'XVXkQGKsFpJk9tHbMJHZdZgTBNbLrgCjW3f3XL4hQLFLbjHJq6QvLc64h82Zzp2d'

loaded_content = Loader(API_KEY, API_SECRET)
ACCES_TOKEN = loaded_content.ACCES_TOKEN
ACCES_TOKEN_SECRET = loaded_content.ACCES_TOKEN_SECRET

class Filter(): ...

class Proces(): ...
"AI dingen"

class Upload(): ... 