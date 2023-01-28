import pandas as pd
import numpy as np
from scipy import stats
import math
import tensorflow as tf

def real_imaginary(impedance : np.array, phase : np.array):
    return impedance * np.cos(np.radians(phase)), impedance * np.sin(np.radians(phase))

def average_data(filename : str, len=4):
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
        'DI Water' : [1, 0, 0, 0, 0],
        'Tap Water' : [0, 1, 0, 0, 0],
        'Polystyrene' : [0, 0, 1, 0, 0],
        'Nitrate' : [0, 0, 0, 1, 0],
        'Sunscreen' : [0, 0, 0, 0, 1]
    }
    return np.array(dict[type])

def train_test_split(filename : str, type):
    train = prepare_data(filename)
    test = pd.read_csv(f'{filename}_5.csv')

def create_data_matrix(filenames, types):
    X = np.array(511, len(filenames), 2)
    for i in range(len(filenames)):
        df = pd.read_csv(filenames[i])
        impedance = np.array(df['Impedance'])
        phase = np.array(df['Phase'])
        entry = np.array(511, 2)
        entry[0] = impedance
        entry[1] = phase
        X[:, i, :] = entry
    y = np.array(len(types), 5)
    for i in range(len(types)):
        y[i] = types[i]

    return X, y


