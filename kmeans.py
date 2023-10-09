from sklearn.cluster import KMeans
import umap #also pip install umap-learn
import numpy as np
import matplotlib.pyplot as plt
from embeddings import Faces
import pickle

class Kmeans_cluster():
        
    def __init__(self, range: tuple=(40, 65), pickle_file="deepface_data.pickle"):
        self.pickle_file = "deepface_data.pickle" #change later
        self.range = range
            
        with open('deepface_data.pickle', 'rb') as pickle_file:
            self.faces = pickle.load(pickle_file)

    def preprocess(self):
        " Prepares the data for the clustering by reducing demensions using umap"
        umap_model = umap.UMAP(n_components=100)
        print(np.array(self.faces[0].embedding).shape)
        quit(0)
        # Ensure embeddings have consistent shape
        embeddings_list = [np.reshape(x.embedding, (x.embedding.shape[0], -1)) for x in self.faces]
        print(embeddings_list[0].shape)
        # Now you can proceed with UMAP
        embeddings_umap = umap_model.fit_transform(embeddings_list)

        embeddings_umap = umap_model.fit_transform(embeddings_list)
        print(embeddings_umap[0].shape)
        return embeddings_umap


    def elbow(self):
        data = self.preprocess()

        raise
        

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



        


kmean = Kmeans_cluster()
kmean.elbow()