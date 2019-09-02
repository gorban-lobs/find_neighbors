import hnswlib
import numpy as np


class NeighborIndex(hnswlib.Index):
    def __init__(self, users, dim=3,
                 num_elems=10000000, ef=200, M=16, space='l2'):
        self.EARTH_RAD = 6371
        self.num_elems = num_elems
        super().__init__(space=space, dim=dim)
        super().init_index(max_elements=num_elems,
                           ef_construction=ef, M=M)
        if users:
            data = []
            data_labels = []
            for u in users:
                data_labels.append(u[0])
                data.append([u[2], u[3]])
            self.add_items(data, data_labels)

    def add_items(self, coords, ind):
        np_labels = np.array(ind)
        np_data = np.array(coords)
        np_data = np.apply_along_axis(self.circle_to_3d_coords, 1, np_data)
        super().add_items(np_data, np_labels)

    def search_neighbors(self, lon, lat, radius, limit):
        super().set_ef(min(limit * 2, self.num_elems))
        coords = np.array([[lon, lat]])
        coords = np.apply_along_axis(self.circle_to_3d_coords, 1, coords)
        labels, distance = super().knn_query(coords[0], k=limit)
        distance = np.sqrt(distance)
        distance = np.apply_along_axis(self.chord_to_circle_dist, 1, distance)
        labels = labels[0][:len(distance[distance <= radius])]
        return labels

    def circle_to_3d_coords(self, coords):
        coords = coords * np.pi / 180
        x = self.EARTH_RAD * np.cos(coords[1]) * np.cos(coords[0])
        y = self.EARTH_RAD * np.cos(coords[1]) * np.sin(coords[0])
        z = self.EARTH_RAD * np.sin(coords[1])
        return [x, y, z]

    def chord_to_circle_dist(self, chord):
        angle = 2 * np.arcsin(chord / (2 * self.EARTH_RAD))
        return angle * self.EARTH_RAD
