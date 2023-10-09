from sklearn.cluster import DBSCAN
import umap #also pip install umap-learn
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from embeddings import Faces
import pickle

class Kmeans_cluster():
        
    def __init__(self, range: list=[40, 65], pickle_file="deepface_data.pickle"):
        self.pickle_file = "deepface_test_data.pickle" #change later
        self.range = range
            
        with open(self.pickle_file, 'rb') as pickle_file:
            self.faces = pickle.load(pickle_file)

    def preprocess(self, DIMENSIONS):
        " Prepares the data for the clustering by reducing demensions using umap"
        umap_model = umap.UMAP(n_components=DIMENSIONS)
        for face in self.faces:
            face.umap_embedding = umap_model.fit_transform(face.embedding.reshape(1, -1))

        if os.path.exists("deepface_umap.pickle"):
            os.remove("deepface_umap.pickle")

        with open("deepface_umap.pickle", "wb") as file:
            pickle.dump(self.faces, file)



    def elbow(self):
        
        with open("deepface_umap.pickle", "rb") as file:
            self.faces = pickle.load(file)
        umap_embeddings = [face.umap_embedding for face in self.faces]
        print(umap_embeddings[0])
        print(self.faces[0].embedding)
        raise
        start, stop = self.range
        x_values = range(start, stop)
        imgs = []
        clusters = DBSCAN(eps=0.05, min_samples=1, metric='cosine').fit(umap_embeddings)
        for i, face in enumerate(self.faces):
            face.label = clusters[i]
            if face.label == 44:
                imgs.append(face.img)

        for image_path in imgs:
            img = mpimg.imread(image_path)  # Read the image
            plt.imshow(img)  # Display the image
            plt.title(image_path)  # Set the title to the image path
            plt.show()  # Show the image
        # kmeans.fit(umap_embeddings)
        # inertia.append(kmeans.inertia_)
        # print(k)
        # self.plot_elbow(inertia)

    def plot_elbow(self, inertia):
        start, stop = self.range
        x_values = range(start, stop)
        plt.plot(x_values, inertia, marker='o')
        plt.title('Elbow Method for Optimal k')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Inertia')
        plt.show()



    