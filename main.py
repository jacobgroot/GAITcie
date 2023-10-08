'''Imports filtered images and calls facial recognition, than saves the files to local system.  '''
from smugloader import Loader
from 
from api import API_KEY, API_SECRET, ACCES_TOKEN, ACCES_TOKEN_SECRET

DOWNLOAD = False
DEEPFACE = False

if DOWNLOAD:
    loaded_content = Loader(API_KEY, API_SECRET, ACCES_TOKEN, ACCES_TOKEN_SECRET)
    loaded_content.download()

if DEEPFACE:

class Proces(): ...
"AI dingen"

class Upload(): ... 