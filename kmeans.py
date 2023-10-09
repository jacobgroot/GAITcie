from sklearn.cluster import KMeans
import umap #also pip install umap-learn
import numpy as np
import matplotlib.pyplot as plt
import os
from embeddings import Faces
import pickle

class Kmeans_cluster():
        
    def __init__(self, range: tuple=(40, 65), pickle_file="deepface_data.pickle"):
        self.pickle_file = "deepface_data.pickle" #change later
        self.range = range
            
        with open(self.pickle_file, 'rb') as pickle_file:
            self.faces = pickle.load(pickle_file)

    def preprocess(self, DIMENSIONS):
        " Prepares the data for the clustering by reducing demensions using umap"
        umap_model = umap.UMAP(n_components=DIMENSIONS)
        embeddings_list = [x.embedding for x in self.faces]

        # Now you can proceed with UMAP
        embeddings_umap = umap_model.fit_transform(embeddings_list)

        embeddings_umap = umap_model.fit_transform(embeddings_list)
        print(embeddings_umap[0].shape)
        
        if os.path.exists("deepface_umap.pickle"):
            os.remove("deepface_umap.pickle")

        with open("deepface_umap.pickle", "wb") as file:
            pickle.dump(embeddings_list, file)



    def elbow(self):
        

        inertia = []
        
        for i in range(self.range):
            kmeans = KMeans(n_clusters=k, random_state=0, n_init="auto")
            kmeans.fit(embeddings_list)
            inertia.append(kmeans.inertia_)
            print(i)

    def plot_elbow(self, inertia):
        plt.plot(range(self.range), inertia, marker='o')
        plt.title('Elbow Method for Optimal k')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Inertia')
        plt.show()



    