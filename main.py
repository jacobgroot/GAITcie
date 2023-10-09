'''Imports filtered images and calls facial recognition, than saves the files to local system.  '''
from smugloader import Loader
from embeddings import Analyse
from kmeans import Kmeans_cluster
from api import API_KEY, API_SECRET, ACCES_TOKEN, ACCES_TOKEN_SECRET

DOWNLOAD = False
DEEPFACE = False
CREATE_TEST_SET = False
KMEANS = True
PREPROCESS = True
DIMENSIONS = 8
PICKLE_FILE_NAME = "deepface_data.pickle"

if DOWNLOAD:
    loaded_content = Loader(API_KEY, API_SECRET, ACCES_TOKEN, ACCES_TOKEN_SECRET)
    loaded_content.download()

if DEEPFACE:
    analyser = Analyse(PICKLE_FILE_NAME, CREATE_TEST_SET)
    analyser.analyse()

if KMEANS:
    cluster = Kmeans_cluster()
    if PREPROCESS:
        cluster.preprocess(DIMENSIONS)
    cluster.elbow()

class Proces(): ...
"AI dingen"

class Upload(): ... 