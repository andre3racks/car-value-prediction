import random
import numpy as np  # linear algebra
import pandas as pd  # data processing / input output file operations
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split


def get_clean_sample_data():

    data = pd.read_csv("NeuralNetwork/autos.csv", encoding = "ISO-8859-1") # Reading data
    
    # because the number of pictures is the same in all advertisements.
    input_data=data.drop('nrOfPictures',1)  
    input_data=input_data[input_data['seller']=='privat']    
    input_data=input_data[input_data['offerType']=='Angebot']
    input_data=input_data.drop(['seller','offerType'],1) 
    #private offers are removed because they are few

    input_data=input_data[input_data['gearbox']!=''] 
    input_data=input_data[input_data['vehicleType']!='']
    input_data=input_data[input_data['fuelType']!='']
    input_data=input_data[input_data['notRepairedDamage']!='']

    model_set=set(input_data.model.str.upper())
    #model_set.remove('')
    input_data.name=input_data.name.str.upper()
    input_data.name=input_data.name.str.split('_')

    print("starting iteration through data")
    # Those that do not have a model name are assigned a name in the name field.
    for index,row in input_data.iterrows():        
        if input_data.model[index]=='':
            for name_pcs in input_data.name[index]:
                if name_pcs in model_set:
                    input_data.loc[index,'model']=name_pcs
                    break

    print("dropping uneeded data")
    input_data=input_data[input_data['model']!='']
    input_data.model=input_data.model.str.upper()
    input_data.brand=input_data.brand.str.upper()
    input_data=input_data.drop('name',1)  
    #Name is dropped because it is not needed.
    input_data=input_data[input_data['price']!=0]
    input_data=input_data[(input_data.powerPS>0) & (input_data.powerPS<=1500)]
    input_data=input_data[(input_data.yearOfRegistration>=1950) & (input_data.yearOfRegistration<2017)]
    input_data=input_data[input_data['monthOfRegistration']!=0]
    input_data=input_data[input_data.price<input_data.price.quantile(0.999)]    
    #%1 top prices subtracted
    # Date values are converted to string and then converted to numerical data.
    input_data.dateCrawled=pd.to_datetime(input_data.dateCrawled)          
    level_dateCrawled=input_data['dateCrawled'].min()-np.timedelta64(1,'D')
    input_data.dateCrawled=(input_data['dateCrawled'] - level_dateCrawled)/np.timedelta64(1,'D')

    input_data.dateCreated=pd.to_datetime(input_data.dateCreated)
    level_dateCreated=input_data['dateCreated'].min()-np.timedelta64(1,'D')
    input_data.dateCreated=(input_data['dateCreated'] - level_dateCreated)/np.timedelta64(1,'D')

    input_data.lastSeen=pd.to_datetime(input_data.lastSeen)
    level_lastSeen=input_data['lastSeen'].min()-np.timedelta64(1,'D')
    input_data.lastSeen=(input_data['lastSeen'] - level_lastSeen)/np.timedelta64(1,'D')

    input_data.postalCode=input_data.postalCode.apply(lambda x: str(int(x/1000))) 
    #postal code is arranged to stay in the first 2 digits.
    input_data.monthOfRegistration=input_data.monthOfRegistration.apply(lambda x: str(x))

    print("There are {} records available for processing in the database.".format(len(input_data)))
        
    #Price is being transferred to a new set
    price_data=input_data['price']  
    #price subtracted from other table
    features_data=input_data.drop('price',1)


    scaler = MinMaxScaler()  
    # It resizes to 0-1 for easier processing of data.
    numerical = ['yearOfRegistration', 'powerPS', 'kilometer','dateCrawled','dateCreated','lastSeen']
    features_data[numerical] = scaler.fit_transform(input_data[numerical])   
    # Creating dummy variables for categorical data.
    features_data = pd.get_dummies(features_data)  
    encoded = list(features_data.columns) 
    print("There are {} features after one hot encoding".format(len(encoded))) 

    X_train_val, X_test, y_train_val, y_test = train_test_split(features_data, price_data, test_size = 0.2, random_state = 0)

    data = {}

    data['X_train'] = X_train_val
    data['Y_train'] = y_train_val
    data['X_test'] = X_test
    data['Y_test'] = y_test

    return data
    
