import pandas as pd
import numpy as np

from normalizers.make_and_model_cleaner import MakeAndModelNormalizer
from encoders.one_hot_encoder import OneHotEncoder

'''
Data loss per column on NaN, 'other' and missing columns
manufacturer: 4.503238211322791%
model: 1.5302640783866006%
year: 0.3242503186708934%

##Results below this had NaN manufacture, model and year removed
condition: 40.38289928226915%
cylinders: 33.92605894042998%
fuel: 4.094514915772008%
title_status: 0.6796818114628844%
transmission: 3.8935940742038433%
drive: 20.421933767293154%
type: 21.95703469306194%
paint_color: 24.355766756633944%
odometer: 17.750505366975823%
'''
def data_set_loss(df, columns):
    print("Data loss per column on NaN, 'other' and missing columns")
    for column in columns:
        new_df = df[df[column].notna()]
        new_df = new_df[new_df[column] != 'other']
        new_df = new_df[new_df[column] != 'missing']

        len_new_df = len(new_df.index)
        percentage_loss = (1 - len_new_df/len(df.index))* 100
        print("{}: {}%".format(column, percentage_loss))

def drop_nan_rows(df, columns):
    for column in columns:
        df = df[df[column].notna()]
    return df

def main():
    #Read CSV into data frame
    feature_columns = ['region', 'price', 'year', 'manufacturer',
                       'model', 'condition', 'cylinders', 'fuel', 'odometer',
                       'title_status', 'transmission', 'drive', 'size',
                       'type', 'paint_color', 'description', 'county', 'state']

    df = pd.read_csv('data/csv/vehicles_clean.csv', names=feature_columns, delimiter=',')
    
    
    #Remove columns that aren't useful
    df = df.drop(columns=['county', 'state', 'description', 'size']) #lose 2/3 of data if "size" is included

    
    # #Normalize Rows (Drop row with NaN values if needed)
    df = drop_nan_rows(df, ['manufacturer', 'model', 'year', 'price', 'odometer'])

    # df = MakeAndModelNormalizer(df, 'data/normalizers/mappings/model_mappings.json').normalize() # only 10% of models don't match!

    # #One Hot Encode Categorical Columns
    # OneHotEncoder(df).encode(['manufacturer', 'model']) # Need to add more categorical data
    # # Save to CSV


main()

