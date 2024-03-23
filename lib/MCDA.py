import pandas as pd
import math
import numpy as np

class MCDA:
    @staticmethod
    def Hellwig(alternatives, ideal_solution, distance_metric, criteria_weights):
        alternatives_df = pd.DataFrame(alternatives)
        for i, criterion in enumerate(alternatives_df.columns):
            max_val = alternatives_df[criterion].max()
            min_val = alternatives_df[criterion].min()
            alternatives_df[criterion] = 1 - abs(ideal_solution[i] - alternatives_df[criterion])/(max_val - min_val)
            ideal_solution[i] = 1
        synth_vars = {}
        for i in range(len(alternatives_df)):
            alternatives_df.at[alternatives_df.index[i], 'di0'] = distance_metric(alternatives_df.iloc[i, 0:len(ideal_solution)], ideal_solution, criteria_weights, alternatives_df.iloc[:,0:len(ideal_solution)])
        _d0 = alternatives_df['di0'].sum() / len(alternatives_df)
        Sd0 = math.sqrt(((alternatives_df['di0'] - _d0) ** 2 / len(alternatives_df)).sum())
        d0 = _d0 + 2 * Sd0
        for i in range(len(alternatives_df)):
            synth_vars[i] = 1 - alternatives_df.at[alternatives_df.index[i], 'di0'] / d0
        return synth_vars

    @staticmethod
    def AHP(criteriaMatrix, optionMatrices, distance_metric):
        pass

    @staticmethod
    def AHPMatrixConsistencyFactor(matrix):
        r_factors = \
            {
                3: 0.58,
                4: 0.90,
                5: 1.12,
                6: 1.24,
                7: 1.32,
                8: 1.41,
                9: 1.45,
                10:1.49
            }
        max_eigen_val = float('-inf')
        for val in np.linalg.eig(np.matrix(matrix))[0]:
            if val == val.real and val.real > max_eigen_val:
                max_eigen_val = val
        m = len(matrix)
        if m > 10 or m < 3:
            r = 1
        else:
            r = r_factors[m]
        return (max_eigen_val - m)/(r *(m-1))