import math
import numpy as np
class Distance:

    @staticmethod
    def Mahalanobis(solution, ideal_solution, criteria_weights, all_data):
        diff = np.matrix(solution.to_numpy() - ideal_solution, dtype=np.float64)
        weights = np.diag(criteria_weights ** 0.5)
        cov = np.matrix(np.cov(all_data.to_numpy()), dtype=np.float64)
        dist = np.matmul(np.matmul(np.matmul(np.matmul(diff, weights), cov.I), weights.transpose()), diff.transpose())
        return abs(dist.item((0, 0))) ** 0.5

    @staticmethod
    def Euclidean(solution, ideal_solution, criteria_weights, all_data):
        dist = 0.0
        for i in range(len(criteria_weights)):
            dist = dist + ((solution[i] - ideal_solution[i])**2) * criteria_weights[i]
        return math.sqrt(dist)
