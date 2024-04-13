import numpy as np

class Util:

    @staticmethod
    def eig(matrix):
        A = np.matrix(matrix)
        sums = A.sum(axis=0)
        matrix_norm = np.matrix([[A[i, j] / sums[0, j] for j in range(len(A))] for i in range(len(A))])
        eig_vec = [matrix_norm[i].mean() for i in range(len(matrix_norm))]
        return np.matrix(eig_vec)

    @staticmethod
    def eig_val(matrix):
        eig_vec = Util.eig(matrix)
        x = matrix * eig_vec.T
        return np.array([x[i, 0] / eig_vec[0, i] for i in range(len(x))]).sum() / len(x)