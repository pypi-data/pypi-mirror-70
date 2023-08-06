import numpy as np
from cobras_ts.superinstance import SuperInstance




class SuperInstance_kmeans(SuperInstance):

    def __init__(self, data, indices, train_indices, parent=None):
        """
            Chooses the super-instance representative as the instance closest to the super-instance centroid
        """
        super(SuperInstance_kmeans, self).__init__(data, indices, train_indices, parent)

        self.centroid = np.mean(data[indices, :], axis=0)
        self.si_train_indices =  [x for x in indices if x in train_indices]

        try:
            self.representative_idx = min(self.si_train_indices, key=lambda x: np.linalg.norm(self.data[x, :] - self.centroid))
        except:
            raise ValueError('Super instance without training instances')



    def distance_to(self, other_superinstance):
        """
            The distance between two super-instances is equal to the distance between there centroids  
        """
        return np.linalg.norm(self.centroid - other_superinstance.centroid)

