import numpy as np
import pandas as pd
from .map import Map
from tqdm.auto import tqdm


class Classification:
    """
    Clasification class. Holds information about what has been classified.
    """
    def __init__(self, som: Map, classification_data, other=None, tagged=False, verbose=1):
        """Creates and classifies some data on top of the som map

        :param som: Map instance which will be responsible of the classification
        :param classification_data:
        :param other:
        :param tagged:
        :param verbose:
        """
        pd.options.mode.chained_assignment = None  # default='warn'

        # If the input data is tagged, keep all the tags; if not, create them
        if tagged:
            self.classification_labels = classification_data[:, 0]
            self.classification_data = classification_data[:, 1:]
        else:
            self.classification_data = classification_data
            self.classification_labels = np.arange(classification_data.shape[0])

        if verbose == 2:
            print("\n\nTags: \n" + str(self.classification_labels))
            print("\n\nClassification data: \n" + str(self.classification_data))

        # Declaration and initialization
        self.activations_map = np.zeros((som.map_size, som.map_size), dtype=int)
        self.distances_map = np.zeros((som.map_size, som.map_size), dtype=float)
        num = 0
        self.topological_map = np.zeros((som.map_size, som.map_size), dtype=float)
        self.umatriz = np.zeros((som.map_size * 2 - 1, som.map_size * 2 - 1), dtype=float)
        self.topological_error = 0
        self.quantization_error = 0
        self.topological_error_map = np.zeros((som.map_size, som.map_size), dtype=float)
        self.quantization_error_map = np.zeros((som.map_size, som.map_size), dtype=float)

        structure = {
            'labels': self.classification_labels.tolist(),
            'data': self.classification_data.tolist(),
            'x': np.zeros(self.classification_data.shape[0], dtype=int).tolist(),
            'y': np.zeros(self.classification_data.shape[0], dtype=int).tolist(),
            'dist': np.zeros(self.classification_data.shape[0], dtype=float).tolist()
        }

        self.classification_map = pd.DataFrame(structure)

        if other is not None:
            self.classification_map = pd.concat([self.classification_map, other], axis=1)

        # Input all the patterns
        for pattern in tqdm(range(0, self.classification_data.shape[0])):
            # Getting the BMU neuron
            bmu, bmu_pos, second_bmu, second_bmu_pos = som.calculate_bmu(self.classification_data[pattern])

            # If the second best neuron is inside the
            if Map.vector_distance(np.array(bmu_pos), np.array(second_bmu_pos)) > 1:
                self.topological_map[bmu_pos] += 1

            # Saving information in the maps
            distance = Map.vector_distance(som.weights[bmu_pos], self.classification_data[pattern])
            self.activations_map[bmu_pos] += 1
            self.distances_map[bmu_pos] += distance

            self.classification_map['x'][pattern] = bmu_pos[0]
            self.classification_map['y'][pattern] = bmu_pos[1]
            self.classification_map['dist'][pattern] = distance

        # Number of neurons that have identified pattern
        self.num_activations = np.count_nonzero(self.activations_map != 0)

        # Calculating the mean of the distances in all the map (only for neurons that have identified a pattern)
        self.mean_distance_map = np.sum(self.distances_map) / self.num_activations

        # Decreasing the number of decimal places to 5
        self.distances_map = np.around(self.distances_map, decimals=5)

        # Calculating topological error and map
        self.topological_error = np.sum(self.topological_map) / np.sum(self.activations_map)
        self.topological_error_map = np.divide(self.topological_map, self.activations_map,
                                               where=self.activations_map != 0)

        # Calculating quantization error and map
        self.quantization_error = np.sum(self.distances_map) / np.sum(self.activations_map)
        self.quantization_error_map = np.divide(self.distances_map, self.activations_map,
                                                where=self.activations_map != 0)

        # Calculate U-Matrix for distance representation
        pesos = np.pad(som.weights, ((1, 1), (1, 1), (0, 0)), 'edge')

        size = som.map_size * 2 - 1

        aux_umatrix = np.zeros([size + 2, size + 2])
        for j in range(1, pesos.shape[0] - 1):
            for i in range(1, pesos.shape[1] - 1):
                x = 2 * i - 1
                y = 2 * j - 1

                aux_umatrix[x - 1, y] = Map.vector_distance(pesos[i, j], pesos[i - 1, j])
                aux_umatrix[x, y + 1] = Map.vector_distance(pesos[i, j], pesos[i, j + 1])
                aux_umatrix[x - 1, y + 1] = (Map.vector_distance(pesos[i, j],
                                                                 pesos[i - 1, j + 1]) + Map.vector_distance(
                                                                 pesos[i - 1, j], pesos[i, j + 1])) * 0.5

        self.umatriz = aux_umatrix[1:-1, 1:-1]
