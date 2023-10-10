from sklearn.cluster import DBSCAN
import umap #also pip install umap-learn
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')  # Use the 'Agg' backend
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting functionality
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import os
from embeddings import Faces
import shutil
import pickle

class Kmeans_cluster():
        
    def __init__(self, range: list=[40, 65], pickle_file="deepface_data.pickle"):
        self.pickle_file = "deepface_test_data.pickle" #change later
        self.range = range
            
        with open(self.pickle_file, 'rb') as pickle_file:
            self.faces = pickle.load(pickle_file)

    def preprocess(self, DIMENSIONS):
        " Prepares the data for the clustering by reducing demensions using umap"

        # create model
        umap_model = umap.UMAP(n_components=DIMENSIONS)

        # extract embeddings
        embedding_list = []
        for face in self.faces:
            embedding_list.append(face.embedding)

        # generate new embeddings
        umap_embedding = umap_model.fit_transform(embedding_list)

        # store embeddings
        for i, face in enumerate(self.faces):
            face.umap_embedding = umap_embedding[i]
        if os.path.exists("deepface_umap_test.pickle"):
            os.remove("deepface_umap_test.pickle")

        with open("deepface_umap_test.pickle", "wb") as file:
            pickle.dump(self.faces, file)



    def elbow(self):
        """
        No longer elbow method, change later
        DBSCAN not working that well, either more/less dimensions needed or smaller eps
        """
        
        with open("deepface_umap_test.pickle", "rb") as file:
            self.faces = pickle.load(file)
        umap_embeddings = [face.umap_embedding for face in self.faces]

        clusters = DBSCAN(eps=0.00005, min_samples=1, metric='cosine').fit(umap_embeddings)
        print(clusters.labels_)

        # # safe in specific cases for testing
        # output_folder = os.path.join(os.getcwd(), "labeled_pictures")
        # for i, face in enumerate(self.faces):
        #     face.label = clusters.labels_[i]
        #     if i == 16 or i == 14 or i == 92 or i == 18 or i == 94 or i == 6 or i == 84: 
        #         shutil.copy(face.image_path, output_folder)

    def plot_elbow(self, inertia):
        start, stop = self.range
        x_values = range(start, stop)
        plt.plot(x_values, inertia, marker='o')
        plt.title('Elbow Method for Optimal k')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Inertia')
        plt.show()



    