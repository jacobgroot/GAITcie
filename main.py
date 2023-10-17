'''Imports filtered images and calls facial recognition, than saves the files to local system.  '''
# from smugloader import Loader
from filter_face import Face_creator
# from api import API_KEY, API_SECRET, ACCES_TOKEN, ACCES_TOKEN_SECRET

# DOWNLOAD = False
# DEEPFACE = True
# CREATE_TEST_SET = False
# KMEANS = False
# PREPROCESS = False
# DIMENSIONS = 100
# PICKLE_FILE_NAME = "deepface_data.pickle"
# min_n_dimensions = 2
# max_n_dimensions = 100
# eps_values = [0.05, 0.005, 0.0005, 0.00005, 0.000005]


# if DOWNLOAD:
#     loaded_content = Loader(API_KEY, API_SECRET, ACCES_TOKEN, ACCES_TOKEN_SECRET)
#     loaded_content.download()

analyser = Face_creator()


# class Proces(): ...
# "AI dingen"

# class Upload(): ... 