'''Imports filtered images and calls facial recognition, than saves the files to local system.  '''
from smugloader import Loader
from api import API_KEY, API_SECRET, ACCES_TOKEN, ACCES_TOKEN_SECRET



loaded_content = Loader(API_KEY, API_SECRET, ACCES_TOKEN, ACCES_TOKEN_SECRET)
loaded_content.download()

class Filter(): ...

class Proces(): ...
"AI dingen"

class Upload(): ... 