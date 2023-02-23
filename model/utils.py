import pandas as pd
import numpy as np
from scipy import stats
import math

def real_imaginary(impedance : np.array, phase : np.array):
    return impedance * np.cos(np.radians(phase)), impedance * np.sin(np.radians(phase))

def average_data(filename : str, len : int):
    dfs = [pd.read_csv(f'{filename}_{i + 1}.csv') for i in range(len)]
    dss = [np.array(df[:]) for df in dfs]
    sum = np.zeros(shape=dss[0].shape)
    for ds in dss: sum += ds
    return pd.DataFrame(sum / len, columns=['Frequency', 'Impedance', 'Phase', 'Real', 'Imaginary', 'Magnitude', ' '])

def drop_outliers(dx : pd.DataFrame):
    df = dx[dx['Phase'] > -95]
    return df[(np.abs(stats.zscore(df['Impedance'] * np.sin(np.sin(np.radians(df['Phase']))))) < 1.5)]


def prepare_data(filename : str, len : int):
    drop_outliers(average_data(filename, len)).to_csv(f'{filename}.csv')

def type_dict(type : str):
    dict = {
        'Polystyrene' : [1, 0, 0],
        'Nitrate' : [0, 1, 0],
        'Sunscreen' : [0, 0, 1],
        'Plain': [0, 0, 0],
        'PSS': [1, 0, 1],
        'PNI': [1, 1, 0],
        'SNI': [0, 1, 1]
    }
    return np.array(dict[type])

def create_data_matrix(filenames, types):
    X = np.zeros(shape=(len(filenames), 512, 2))
    for i in range(len(filenames)):
        df = pd.read_csv(filenames[i])
        impedance = np.array(df['Impedance'])
        phase = np.array(df['Phase'])
        entry = np.zeros(shape=(512, 2))
        entry[:, 0] = impedance
        entry[:, 1] = phase
        X[i, :, :] = entry
    X = np.reshape(X, newshape=(len(filenames), 1024))
    y = np.array(types)

    return X, y