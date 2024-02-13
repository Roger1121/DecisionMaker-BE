import math
class Distance:

    @staticmethod
    def Mahalanobis(solution, ideal_solution, criteria_weights):
        return 0.0

    @staticmethod
    def Euclidean(solution, ideal_solution, criteria_weights):
        dist = 0.0
        for i in range(len(criteria_weights)):
            dist = dist + ((solution[i] - ideal_solution[i])**2) * criteria_weights[i]
        return math.sqrt(dist)
