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
        self.pickle_output = 'face_pickle'

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.face_list()


    def face_list(self):
        " Creates a list with all faces and saves each face as seperate image"

        faces = []
        cutout_faces = []
        # get all faces for each image and put them all as a Face instance in a list 
        for i, filename in enumerate(os.listdir(self.media_path)):
            if i == 1:
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
            cutout_faces.append(Face(pil_image, face.original_img))

            # self.save_face(pil_image, j)
        
        self.save_pickle(cutout_faces)

    def save_pickle(self, cutout_faces):
        with open(self.pickle_output, "wb") as file:
            for face_instance in cutout_faces:
                pickle.dump(face_instance, file)
            

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
