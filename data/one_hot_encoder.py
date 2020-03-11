""" USAGE
feature_columns = ['region', 'year', 'price', 'manufacturer', 'model', 'condition', 'cylinders', 'fuel', 'odometer', 'title_status', 'transmission', 'vin', 'drive', 'size', 'type', 'paint_color', 'description', 'county', 'state']
vehicle_data = pd.read_csv("./data/vehicles_clean.csv", names=feature_columns, delimiter=',')
encoder = OneHopEncode(vehicle_data)
print(encoder.encode('manufacturer').head())
"""
class OneHotEncoder:
    def __init__(self, data):
        #data is a pandas DataFrame
        self.data = data

    def encode(self, columns):
        if isinstance(columns,list) or isinstance(columns,tuple):
            for column in columns:
                self.encode_column(column)
        elif isinstance(columns,str):
            self.encode_column(columns)
        else:
            raise TypeError('Must be a string, list or tuple')
        return self.data
    
    def encode_column(self, encode_column):
        new_columns = list(self.data[encode_column].unique())
        #Deals with NaN values in the list
        new_columns = [x for x in new_columns if x == x]
        for new_column in sorted(new_columns):
            self.data[new_column] = 0
            self.data.loc[self.data[encode_column] == new_column, new_column] = 1
        del self.data[encode_column]