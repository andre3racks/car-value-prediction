import json
import re

'''USAGE
from model_cleaner import MakeAndModelCleaner

feature_columns = ['region', 'price','year',  'manufacturer', 'model', 'condition', 'cylinders', 'fuel', 'odometer', 'title_status', 'transmission', 'drive', 'size', 'type', 'paint_color', 'description', 'county', 'state']
vehicle_data = pd.read_csv("./data/csv/vehicles_clean.csv", names=feature_columns, delimiter=',')

clean_data = MakeAndModelCleaner(vehicle_data, './data/mappings/model_mappings.json').normalize()

print(clean_data)
'''
class MakeAndModelNormalizer:
    def __init__(self, data, mapping_path):
        self.data = data
        
        with open(mapping_path, 'r') as file:
            self.mappings = json.load(file)
    
    def normalize(self):
        #remove rows that dont have a make that matches
        self.prune_makes()
        
        #remove rows that dont have a model that matches
        self.prune_models()
        self.normalize_models()
        # return data
        return self.data

    def prune_makes(self):
        # remove NaN models
        self.remove_nan_for('manufacturer')
        # remove bike/other models (not in mappings) from list
        self.data = self.data.loc[self.data['manufacturer'].isin(list(self.mappings.keys()))]

    def prune_models(self):
        # remove NaN models
        self.remove_nan_for('model')
        # remove models not in mappings
        self.data = self.data.loc[self.data[['manufacturer','model']].apply(lambda value: bool(self.find_model_substrings(*value)), axis=1)]

    def normalize_models(self):
        self.data['model'] = self.data[['manufacturer','model']].apply(lambda value: self.find_model_substrings(*value)[0], axis=1)

    def find_model_substrings(self, make, model):
        return sorted([self.mappings[make][accepted_value] for accepted_value in self.mappings[make].keys() if accepted_value in simplify_string(model)], reverse=True, key=len )

    def remove_nan_for(self, column):
        self.data = self.data[self.data[column].notna()]

# downcases and removes symbols(non-word characters) from a string
def simplify_string(string):
    return re.sub(r'\W','',string.lower()) 