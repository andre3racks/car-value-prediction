from sklearn.model_selection import train_test_split
import random
import numpy as np  # linear algebra
import pandas as pd  # data processing / input output file operations
import os


def get_splits(csv_path, split):
    if not os.path.isfile(csv_path):
        print("csv {} not found.".format(csv_path))
        return None
    
    print("starting to read csv...")
    data = pd.read_csv(csv_path, delimiter=',', error_bad_lines=False)
    # Drop any Unnamed columns (Should only be the 'id' column)
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
    print("finished reading csv.")

    X = data.drop('price', axis=1)
    Y = data["price"]

    data_dict = {}
    print("splitting data into training and testing sets.")
    data_dict['X_train'], data_dict['X_test'], data_dict['Y_train'],  data_dict['Y_test'] = train_test_split(X, Y, test_size=split)
    return data_dict