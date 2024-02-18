import pandas as pd
import math
class MCDA:
    @staticmethod
    def Hellwig(alternatives, ideal_solution, distance_metric, criteria_weights):
        alternatives_df = pd.DataFrame(alternatives)
        for i, criterion in enumerate(alternatives_df.columns):
            avg = alternatives_df[criterion].mean()
            std_dev = alternatives_df[criterion].std()
            alternatives_df[criterion] = (alternatives_df[criterion]-avg)/std_dev
            ideal_solution[i] = (ideal_solution[i]-avg)/std_dev
        synth_vars = {}
        for i in range(len(alternatives_df)):
            alternatives_df.at[alternatives_df.index[i], 'di0'] = distance_metric(alternatives_df.iloc[i, 0:len(ideal_solution)], ideal_solution, criteria_weights, alternatives_df.iloc[:,0:len(ideal_solution)])
        _d0 = alternatives_df['di0'].sum() / len(alternatives_df)
        Sd0 = math.sqrt(((alternatives_df['di0'] - _d0) ** 2 / len(alternatives_df)).sum())
        d0 = _d0 + 2 * Sd0
        for i in range(len(alternatives_df)):
            synth_vars[i] = 1 - alternatives_df.at[alternatives_df.index[i], 'di0'] / d0
        return synth_vars