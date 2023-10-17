from deepface import DeepFace
import os
import pickle


class Analyse():
    def __init__(self):
        self.input = os.path.join(os.getcwd(), 'face_pickle')
        self.faces = self.__get_face_instances()
        self.unique = {}
        self.matched_faces = set()

    def find_match(self):
        for face in self.faces:
            face_cutout = face.face_img
            for compare_face in self.faces:
                if face == compare_face:
                    continue
                if compare_face.face_img in self.matched_faces:
                    continue
                if compare_face.original_img == face.original_img:
                    continue

                self.unique[face.face_img] = [face.original_img]
                self.matched_faces.add(face.face_img)
                if DeepFace.verify(img1_path=face.face_img, img2_path=compare_face.face_img)['verified']:
                    self.unique[face.face_img].append(compare_face.original_img)
                    self.matched_faces.add(compare_face.face_img)


    def __get_face_instances(self):
        with open(self.input, "rb") as file:
            faces = pickle.load(file)
        return faces