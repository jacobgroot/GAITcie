from sklearn.cluster import DBSCAN
import umap #also pip install umap-learn
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')  # Use the 'Agg' backend
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting functionality
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.metrics import silhouette_score
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
        return umap_embedding # temporary for testing
        # store embeddings
        for i, face in enumerate(self.faces):
            face.umap_embedding = umap_embedding[i]
        if os.path.exists("deepface_umap_test.pickle"):
            os.remove("deepface_umap_test.pickle")

        with open("deepface_umap_test.pickle", "wb") as file:
            pickle.dump(self.faces, file)

    def find_optimal_parameters(self, min_n_dimensions, max_n_dimensions, eps_values, label):
        ''' Tests different parameters on the dimensions of embedding and epsilon for dbscan'''

        best_n_dimensions = 0
        best_eps = 0
        best_silhouette_score = -1
        silhouette_scores = []

        # check all dimensions
        for n_dimensions in range(min_n_dimensions, max_n_dimensions + 1):
            print(n_dimensions)
            # Perform UMAP preprocessing with the current n_dimensions
            self.umap_embeddings = self.preprocess(n_dimensions)

            for _, eps in enumerate(eps_values):
                # Perform DBSCAN clustering with the current eps
                labels = self.density_scan(eps)

                # Evaluate the clustering using silhouette score
                silhouette_score = self.evaluate_clustering(labels)
                silhouette_scores.append(silhouette_score)
                
                
                # Update the best parameters if the silhouette score is improved
                if silhouette_score > best_silhouette_score:
                    best_silhouette_score = silhouette_score
                    best_n_dimensions = n_dimensions
                    best_eps = eps

        print(silhouette_scores)
        if label:
            self.umap_embeddings = self.preprocess(best_n_dimensions)
            labels = self.density_scan(best_eps)
            output_folder = os.path.join(os.getcwd(), "labeled_pictures")
            self.organize_images_by_labels(output_folder, labels)
            
        return best_n_dimensions, best_eps, best_silhouette_score

    def density_scan(self, eps):
        """
        DBSCAN not working that well, either more/less dimensions needed or smaller eps
        Also possible that umap is not optimal. Maybe PCA to focus more on most expressive features
        """
        
        with open("deepface_umap_test.pickle", "rb") as file:
            self.faces = pickle.load(file)
        umap_embeddings = [face.umap_embedding for face in self.faces]

        clusters = DBSCAN(eps=eps, min_samples=1, metric='cosine').fit(umap_embeddings)
        return clusters.labels_

    def evaluate_clustering(self, labels):
        # Silhouette Score
        try: 
            return float(silhouette_score(self.umap_embeddings, labels, metric='cosine'))
        except:
            return -1

    def organize_images_by_labels(self, output_folder, labels):
        """
        Creates for each label a seperate folder to store all images with that label
        In the future, should also store what face was targeted.
        !Warning! will remove all contents of labeled_pictures
        """

        # clear labeled_pictures
        self.clear_folder(output_folder)
            
        # create folders and copy images based on cluster labels
        for i, face in enumerate(self.faces):
            label = labels[i]
            face.label = label

            # store image in folder (create if does not exist)
            label_folder = os.path.join(output_folder, str(label))
            os.makedirs(label_folder, exist_ok=True)
            shutil.copy(face.image_path, label_folder)

    @staticmethod
    def clear_folder(folder):
        " can clear labeled_pictures folder. Can also clear any folder with child folder, so use with caution"
        if os.path.exists(folder):
            for folder_name in os.listdir(folder):
                folder_path = os.path.join(folder, folder_name)
                if os.path.isdir(folder_path):
                    shutil.rmtree(folder_path)

    def plot(self, inertia):
        ''' plotting method that is used to show cost with elbow method'''
        start, stop = self.range
        x_values = range(start, stop)
        plt.plot(x_values, inertia, marker='o')
        plt.title('Elbow Method for Optimal k')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Inertia')
        plt.show()



    