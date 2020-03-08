from sklearn.model_selection import train_test_split
import random
import numpy as np  # linear algebra
import pandas as pd  # data processing / input output file operations
import os

def get_splits(csv_path, split):

    # currently doesn't use 'city' beacuse its a string

    columns = ['city', 'price', 'year', 'make',
                        'model', 'condition', 'cylinders', 'fuel', 'odometer',
                       'title_status', 'transmission', 'drive', 'size',
                       'type', 'paint_color', 'state']


    features = ['year', 'make',
                        'model', 'condition', 'cylinders', 'fuel', 'odometer',
                       'title_status', 'transmission', 'drive', 'size',
                       'type', 'paint_color', 'state']

    if not os.path.isfile(csv_path):
        print("csv {} not found.".format(csv_path))
        return None
    
    data = pd.read_csv(csv_path, names=columns, delimiter=',')

    # removes NOTVALID model rows
    Z = data[columns]
    Z = Z[Z.model != "NOTVALID"]
    # removes values too large error
    Z = Z[Z.price < 2000000]
    Z = Z[Z.odometer < 2000000]
    
    X = Z[features]
    Y = Z.price

    data_dict = {}
    data_dict['X_train'], data_dict['X_test'], data_dict['Y_train'],  data_dict['Y_test'] = train_test_split(X, Y, test_size=split)
    return data_dict