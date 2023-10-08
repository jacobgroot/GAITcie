"""
File calls deepface on all images in folder media/.
!Important! media/ should always be the folder containing images/videos to be analyzed.
The file will create a temporary file with all embeddings (overwriting the previous embedding file).
"""

import os
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

# store all Faces instances
faces = []
local_faces = []
json_filename = "deepface_data.json"

# Remove the previous JSON file if it exists
if os.path.exists(json_filename):
    os.remove(json_filename)

# call DeepFace on each image
media_path = os.path.join(os.getcwd(), 'media')
for filename in tqdm(os.listdir(media_path)):
    img_path = os.path.join(media_path, filename)
    embeddings = [x["embedding"] for x in DeepFace.represent(img_path, enforce_detection=False)]
    faces.append(Faces(embeddings, img_path))
    local_faces.append({
        "embeddings": embeddings,
        "img_path": img_path
    })

# Save the data to a pickle file
with open(json_filename, 'wb') as pickle_file:
    pickle.dump(faces, pickle_file)
