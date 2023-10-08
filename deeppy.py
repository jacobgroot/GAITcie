"""
File contains data architecture and analysis class to create embeddings for images containing persons
those embeddings will be safed to a file (name specified when called and included in .gitignore) and can be used to sort images per person
"""

import os
import multiprocessing
import pickle
from tqdm import tqdm
from deepface import DeepFace
from dataclasses import dataclass, field

@dataclass
class Faces:
    """Each instance represents one image containing information on each person in it."""
    embedding: list
    image_path: str
    labels: list = field(default_factory=list)

class Analyse():
    """ 
    Class analyses every image in the media/ folder with the DeepFace import.
    Creates a pickle file with all the embeddings and the corresponding image
    """

    # CHANGE THIS WHEN YOU RUN ON DIFFERENT PC TO NOT BLOW IT UP
    NUMBER_OF_CORES = 2

    def __init__(self, pickle_file):
        self.faces = []
        self.pickle_file = pickle_file
        self.media_path = os.path.join(os.getcwd(), 'media')

        # Remove the previous pickle file
        if os.path.exists(pickle_file):
            os.remove(pickle_file)

    def process_image(img_path):
        " Returns Faces dataclass with all embeddings per image (n=number of persons in image)"

        embeddings = [x["embedding"] for x in DeepFace.represent(img_path, enforce_detection=False)]
        return Faces(embeddings, img_path)

    def analyse(self):
        " Calls process_image on all images in media folder and stores it in pickle file"
        image_files = [os.path.join(self.media_path, filename) for filename in os.listdir(self.media_path)]

        for img in tqdm(image_files):
            self.faces.append(self.process_image(img))

        # Save the results to a pickle file
        with open(self.pickle_file, "wb") as file:
            pickle.dump(self.faces, file)
