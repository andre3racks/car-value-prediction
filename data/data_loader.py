from sklearn.model_selection import train_test_split
import random
import numpy as np  # linear algebra
import pandas as pd  # data processing / input output file operations
import os

def get_splits(csv_path, split):

    columns = ['id', 'url', 'region', 'region_url', 'price', 'year',
               'manufacturer', 'model', 'condition', 'cylinders', 'fuel',
               'odometer', 'title_status', 'transmission', 'vin', 'drive',
               'size', 'type', 'paint_color', 'image_url', 'description',
               'county', 'state', 'lat', 'long']

    features = ['region', 'year', 'manufacturer',
                        'model', 'condition', 'cylinders', 'fuel', 'odometer',
                       'title_status', 'transmission', 'vin', 'drive', 'size',
                       'type', 'paint_color', 'description', 'county', 'state']

    if not os.path.isfile(csv_path):
        print("csv {} not found.".format(csv_path))
        return None
    
    data = pd.read_csv(csv_path, names=columns, delimiter=',')

    X = data[features]
    Y = data.price

    data_dict = {}
    data_dict['X_train'], data_dict['Y_train'], data_dict['X_test'], data_dict['Y_test'] = train_test_split(X, Y, test_size=split)
    return data_dict