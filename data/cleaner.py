import pandas as pd
import csv
import numpy as np

from normalizers.make_and_model_cleaner import MakeAndModelNormalizer
from encoders.one_hot_encoder import OneHotEncoder

def price_regularize(price):
    return price

def regularize_year(year):
    if year == "" or year == None:
        return -1
    else:
        return 2020-int(year)

def make_index(make):
    if make == "" or make == None:
        return -1
    else:
        makeUpper = make.upper()
        makes = ['ACURA', 'ALFA-ROMEO', 'ASTON-MARTIN', 'AUDI', 'BMW', 'BUICK', 'CADILLAC', 'CHEVROLET', 'CHRYSLER', 'DATSUN', 'DODGE', 'FERRARI', 'FIAT', 'FORD', 'GMC', 'HARLEY-DAVIDSON', 'HENNESSEY', 'HONDA', 'HYUNDAI', 'INFINITI', 'JAGUAR', 'JEEP', 'KIA', 'LAND ROVER', 'LEXUS', 'LINCOLN', 'MAZDA', 'MERCEDES-BENZ', 'MERCURY', 'MINI', 'MITSUBISHI', 'MORGAN', 'NISSAN', 'PONTIAC', 'PORCHE', 'RAM', 'ROVER', 'SATURN', 'SUBARU', 'TESLA', 'TOYOTA', 'VOLKSWAGEN', 'VOLVO']
        return makes.index(makeUpper)

def condition_index(condition):
    conditionUpper = condition.upper()
    conditions = ['NEW', 'LIKE NEW', 'EXCELLENT', 'GOOD', 'FAIR', 'SALVAGE']
    if conditionUpper in conditions:
        return conditionUpper
    else:
        return -1

def cylinders_index(cylinder):
    cylinderUpper = cylinder.upper()
    cylinders = ['3 CYLINDERS', '4 CYLINDERS', '5 CYLINDERS', '6 CYLINDERS', '8 CYLINDERS', '10 CYLINDERS', '12 CYLINDERS', 'OTHER']
    if cylinderUpper in cylinders:
        return cylinderUpper
    else:
        return -1


def gas_index(gas):
    gasUpper = gas.upper()
    gasTypes = ['GAS', 'DIESEL', 'OTHER', 'ELECTRIC', 'HYBRID']
    if gasUpper in gasTypes:
        return gasUpper
    else:
        return -1

def odometer_regularize(odometer):
    return odometer

def title_index(title):
    titleUpper = title.upper()
    titles = ['CLEAN', 'REBUILT', 'SALVAGE', 'LIEN', 'MISSING', 'PARTS ONLY']
    if titleUpper in titles:
        return titleUpper
    else:
        return -1

def transmission_index(transmission):
    transmissionUpper = transmission.upper()
    transmissions = ['MANUAL', 'AUTOMATIC', 'OTHER']
    if transmissionUpper in transmissions:
        return transmissionUpper
    else:
        return -1

def drive_index(drive):
    driveUpper = drive.upper()
    drives = ['4WD', 'FWD', 'RWD']
    if driveUpper in drives:
        return driveUpper
    else:
        return -1

def size_index(size):
    sizeUpper = size.upper()
    sizes = ['COMPACT', 'SUB-COMPACT', 'MID-SIZE', 'FULL-SIZE']
    if sizeUpper in sizes:
        return sizeUpper
    else:
        return -1

def type_index(typee):
    typeUpper = typee.upper()
    types = ['HATCHBACK', 'PICKUP', 'SUV', 'SEDAN', 'TRUCK', 'WAGON', 'VAN', 'COUPE', 'CONVERTIBLE', 'OTHER', 'OFFROAD', 'MINI-VAN', 'BUS']
    if typeUpper in types:
        return typeUpper
    else:
        return -1

def color_index(color):
    colorUpper = color.upper()
    colors = ['BLACK', 'WHITE', 'SILVER', 'BROWN', 'BLUE', 'GREY', 'RED', 'CUSTOM', 'PURPLE', 'YELLOW', 'GREEN', 'ORANGE']
    if colorUpper in colors:
        return colorUpper
    else:
        return -1

def state_index(state):
    upperState = state.upper()
    states = ["AL","AK","AZ","AR","CA","CO","CT","DC","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
    if upperState in states:
        return upperState
    else:
        return -1

def regularize_data(cur_row):
    cur_row[0] = price_regularize(cur_row[0])# Price
    cur_row[1] = regularize_year(cur_row[1]) # Change year to number of years old
    cur_row[2] = make_index(cur_row[2]) # Change make of car to number
    cur_row[3] = cur_row[3] # Change model of car to number
    cur_row[4] = condition_index(cur_row[4])# Condition
    cur_row[5] = cylinders_index(cur_row[5])# Cylinders
    cur_row[6] = gas_index(cur_row[6])# Gas type
    cur_row[7] = odometer_regularize(cur_row[7])# Odometer
    cur_row[8] = title_index(cur_row[8])# Title Status
    cur_row[9] = transmission_index(cur_row[9])# Transmission (Manual/Auto)
    cur_row[10] = drive_index(cur_row[10])# Drive (4wd, fwd, rwd)
    cur_row[11] = size_index(cur_row[11])# Size
    cur_row[12] = type_index(cur_row[12])# Type
    cur_row[13] = color_index(cur_row[13])# Color
    cur_row[14] = state_index(cur_row[14]) # State
    return cur_row

def model_index(makeIndex, model):
    if makeIndex == 0:
        return acura(model)
    if makeIndex == 1:
        return alfa_romeo(model)
    if makeIndex == 2:
        return aston_martin(model)
    if makeIndex == 3:
        return audi(model)
    if makeIndex == 4:
        return bmw(model)
    if makeIndex == 5:
        return buick(model)
    else:
        return "Model"

def model_list():
    models = []
    trimmed_models = []
    for i in range(43):
        models.append([])
        trimmed_models.append([])

    with open('vehicles_clean.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            makeIndex = make_index(row[3].upper())
            if makeIndex != -1:
                if row[4] not in models[makeIndex]:
                    models[makeIndex].append(row[4])


def clean_clean_data():
    clean_data = []
    with open('vehicles_clean.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            regular_row = regularize_data(row)
            clean_data.append(regular_row)
    return clean_data

def load_data_csv():
    clean_data = []
    with open('vehicles.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            if int(row[4]) > 0:
                cur_row = [row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[15], row[16], row[17], row[18], row[22]]
                regular_row = regularize_data(cur_row)
                clean_data.append(regular_row)
    return clean_data

def save_csv(clean_data):
    with open('vehicles_clean.csv','w') as cleanfile:
        csvwriter = csv.writer(cleanfile)
        for row in clean_data:
            csvwriter.writerow(row)

def drop_nan_rows(df, columns):
    for column in columns:
        df = df[df[column].notna()]
    return df

def model_cleanup():
    feature_columns = ['price', 'year', 'manufacturer',
                           'model', 'condition', 'cylinders', 'fuel', 'odometer',
                           'title_status', 'transmission', 'drive', 'size',
                           'type', 'paint_color', 'state']

    df = pd.read_csv('vehicles_clean.csv', names=feature_columns, delimiter=',')


    #Remove columns that aren't useful
    df = df.drop(columns=['size']) #lose 2/3 of data if "size" is included

    # #Normalize Rows (Drop row with NaN values if needed)
    df = drop_nan_rows(df, ['manufacturer', 'model', 'year', 'price', 'odometer'])
    df = MakeAndModelNormalizer(df, 'normalizers/mappings/model_mappings.json').normalize() # only 10% of models don't match!
    df.to_csv('vehicles_cleaner.csv')


def main():
    clean_data = load_data_csv()
    save_csv(clean_data)
    model_cleanup()

main()