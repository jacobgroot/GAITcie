import deepface
import os

""" File calls deepface on all images in foler media/. 
    !Important! media/ should always be the folder containing images/videos to be analysed
    will return 
    DEV OPTIONS:
    - List with np.arrays per embedding
      Along with /dictionary["embedding"] = image/ style dictionary to store image info 
      that will be accessed when embedding has label
    - List with @Dataclass called "Faces" that has a .embeddings and .images attribute
      No need for the dictionary, will take more effort to construct final list with all embedding
      Final list with all embeddings should probably be constructed when instance of "Faces" is made
      so that list will also be returned  
    """ 