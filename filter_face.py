"""
File contains data architecture and analysis class to create embeddings for images containing persons
those embeddings will be safed to a file (name specified when called and included in .gitignore) and can be used to sort images per person
"""

import os
import multiprocessing
import pickle
import numpy as np
from tqdm import tqdm
from dataclasses import dataclass, field
import cv2
from face_lib import face_lib
import face_recognition
from PIL import Image

@dataclass
class Face:
    """Each instance represents one image containing information on each person in it."""
    face_img: list
    original_img: list

class Face_creator():
    
    def __init__(self):
        self.faces = []
        self.media_path = os.path.join(os.getcwd(), 'media') 
        self.output_folder = 'separate_faces'

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.face_list()


    def face_list(self):
        " Creates a list with all faces and saves each face as seperate image"

        faces = []

        # get all faces for each image and put them all as a Face instance in a list 
        for i, filename in enumerate(os.listdir(self.media_path)):
            if i == 15: # do not make it too large for testing
                break
            img_path = os.path.join(self.media_path, filename)
            
            faces.extend(self.detect_faces(img_path))
            print(len(faces))

        # save each image seperately
        for j, face in enumerate(faces):

            top, right, bottom, left = face.face_img
       
            image = cv2.imread(face.original_img)
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)

            self.save_face(pil_image, j)
            

    def detect_faces(self, image):
        " Detects all faces in an images and stores that face along with original in a list using Face instance "
        img = face_recognition.load_image_file(image)
        face_locations = face_recognition.face_locations(img)
        return [Face(result, image) for result in face_locations]

    def save_face(self, pil_image, index):
        " Saves an image for later analysing purposes"
        if pil_image is not None:
            print("good")
            output_path = os.path.join(self.output_folder, f'face_{index}.jpg')
            pil_image.save(output_path)

            
            
    def write_pickle(self, dump_data):
        with open("deepface_find_test_data", "wb") as file:
            for _, data in dump_data:
                # create test set
                if _ == 100:
                    return
                
                pickle.dump(data, file)

    
    


# class Analyse():
#     """ 
#     Class analyses every image in the media/ folder with the DeepFace import.
#     Creates a pickle file with all the embeddings and the corresponding image
#     """

#     # CHANGE THIS WHEN YOU RUN ON DIFFERENT PC TO NOT BLOW IT UP
#     NUMBER_OF_CORES = 2

#     def __init__(self, pickle_file, CREATE_TEST_SET):
#         self.faces = []
#         self.pickle_file = pickle_file
#         self.media_path = os.path.join(os.getcwd(), 'media')
#         self.CREATE_TEST_SET = CREATE_TEST_SET

#         # Remove the previous pickle file
#         if os.path.exists(pickle_file) and not self.CREATE_TEST_SET:
#             os.remove(pickle_file)

#         if os.path.exists("deepface_test_data.pickle") and self.CREATE_TEST_SET:
#             os.remove("deepface_test_data.pickle")


#     @staticmethod
#     def process_image(img_path):
#         " Returns Faces dataclass with all embeddings per image (n=number of persons in image)"

#         embeddings = DeepFace.represent(img_path, enforce_detection=False)

#         return [Faces(np.array(embedding["embedding"]), img_path) for embedding in embeddings]

#     def analyse(self):
#         " Calls process_image on all images in media folder and stores it in pickle file"

#         image_files = [os.path.join(self.media_path, filename) for filename in os.listdir(self.media_path)]
#         for img in tqdm(image_files):
#             self.faces.extend(self.process_image(img))
#             if self.CREATE_TEST_SET and len(self.faces) >= 100:
#                 with open("deepface_test_data.pickle", "wb") as file:
#                     pickle.dump(self.faces, file)
#                 return

#         # Save the results to a pickle file
#         with open(self.pickle_file, "wb") as file:
#             pickle.dump(self.faces, file)
