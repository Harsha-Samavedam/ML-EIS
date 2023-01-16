import pandas as pd
import numpy as np
from scipy import stats

def real_imaginary(impedance : np.array, phase : np.array):
    return impedance * np.cos(np.radians(phase)), impedance * np.sin(np.radians(phase))

def average_data(filename : str, len : int):
    dfs = [pd.read_csv(f'{filename}_{i + 1}.csv') for i in range(len)]
    dss = [np.array(df[:]) for df in dfs]
    sum = np.zeros(shape=dss[0].shape)
    for ds in dss: sum += ds
    return pd.DataFrame(sum / len, columns=['Frequency', 'Impedance', 'Phase', 'Real', 'Imaginary', 'Magnitude'])

def drop_outliers(df : pd.DataFrame):
    return df[(np.abs(stats.zscore(df[2])) < 3)]




