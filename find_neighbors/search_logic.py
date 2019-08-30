import hnswlib
import numpy as np


class NeighborIndex(hnswlib.Index):
    def __init__(self, users, dim=2,
                 num_elems=10000000, ef=200, M=16, space='l2'):
        self.num_elems = num_elems
        data = []
        data_labels = []
        for u in users:
            data_labels.append(u[0])
            data.append([u[2], u[3]])
        np_data = np.array(data, dtype=np.float32)
        np_labels = np.array(data_labels)
        super().__init__(space=space, dim=dim)
        super().init_index(max_elements=num_elems,
                           ef_construction=ef, M=M)
        super().add_items(np_data, np_labels)

    def add_items(self, coords, ind):
        np_data = np.array([coords])
        np_labels = np.array([ind])
        super().add_items(np_data, np_labels)

    def search_neighbors(self, lon, lat, radius, limit):
        super().set_ef(min(limit * 2, self.num_elems))
        labels, distance = super().knn_query(np.array([lon, lat]), k=limit)
        km_dist = np.sqrt(distance) * 111.11
        labels = labels[0][:len(km_dist[km_dist <= radius])]
        return labels
