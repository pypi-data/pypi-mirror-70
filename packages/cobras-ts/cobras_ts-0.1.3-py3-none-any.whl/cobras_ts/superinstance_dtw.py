import numpy as np

from cobras_ts.superinstance import SuperInstance


def get_prototype(A,indices):
    max_affinity_to_others = -np.inf
    prototype_idx = None

    for idx in indices:
        affinity_to_others = 0.0
        for j in indices:
            if j == idx:
                continue
            affinity_to_others += A[idx,j]
        if affinity_to_others > max_affinity_to_others:
            prototype_idx = idx
            max_affinity_to_others = affinity_to_others

    return prototype_idx


class SuperInstance_DTW(SuperInstance):

    def __init__(self, data, indices, train_indices, parent=None):
        """
            Chooses the super-instance representative based on the affinity matrix under the data argument
        """
        super(SuperInstance_DTW, self).__init__(data, indices, train_indices, parent)
        self.representative_idx = get_prototype(self.data, self.train_indices)

    def distance_to(self, other_superinstance):
        """
            Uses the negative entry in the affinity matrix between the two super-instance representatives

            note: this is not a correct distance measure but this is not necessary for COBRAS
        """
        # not really a distance, but that does not matter for COBRAS execution, this is only used for sorting etc.
        return -self.data[self.representative_idx, other_superinstance.representative_idx]
