class Face():

    def __init__(self, face, img):
        self.face = face
        self.img = img

all_faces = [Face("a", 1), Face("b", 1), Face("c", 2), Face("a", 2), Face("d", 3), Face("c", 3)]
unique_faces = {}

for face in all_faces:
    key_face = None
    raise
    for u_face in unique_faces:
        if deepface.find(face.face, u_face)["verified"]:
            found = True
            key_face = u_face
            break
    if not found:
        key_face = face.face
        unique_faces[face.face] = face.img
    for _face in all_faces:
        if deepface.find(_face.face, face.face)["verified"] and _face.img != face.img:
            unique_faces[key_face].append(_face.img)

