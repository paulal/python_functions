''' Tässä tiedostossa on funktioita, joilla lasketaan 
ravintoaineiden saantia suhteessa ravitsemussuosituksiin.
Ruokien ravintoainesisällöt ovat THL:n ylläpitämän
Fineli-tietokannan versiosta 20. Päivittäiset saantisuositukset
ovat pääosin suomalaisista ravitsemussuosituksista vuodelta 2014
pienin täydennyksin.

Olennaiset tiedot löytyvät seuraavista csv-tiedostoista:

component_value_utf-8.csv - ravintoaineiden määrät kussakin elintarvikkeessa
eufdname_FI_utf-8.csv - ravintoaineiden nimet
food_utf-8.csv - elintarvikkeiden nimet
saantisuositus_2014.csv - päivittäiset saantisuositukset

'''
import pandas as pd
from scipy.optimize import linprog

# pois laskuista jätettävät elintarviketyypit (FUCLASS):
# lastenruoat, äidinmaidonkorvikkeet, ateriankorvikkeet ja lisäravinteet
omitted_food_types = ('BABYFTOT', 
'BABMEATD',
'BABFISHD',
'BABMILPO',
'BABWATPO',
'BABFRUB',
'BABVEGE',
'BABMIFRU',
'BABOTHER',
'MMILK',
'INFMILK',
'CASMILK',
'PREMILK',
'SOYMILK',
'WHEYMILK',
'AMINMILK',
'SPECTOT',
'SPECSUPP',
'MEALREP',
'SPORTFOO',
'SPECFOOD')

def read_files(path:str) -> tuple:
    """This function reads the following csv files and returns 
    a tuple of pandas data structures: 
    component_value_utf-8.csv
    eufdname_FI_utf-8.csv
    food_utf-8.csv
    saantisuositus_2014.csv

    The function also removes data for various supplements,
    since the target is to look at real foods.

    Args:
        path (str): absolute path to csv files

    Returns:
        tuple: Returns a tuple of pandas data structures with the 
        data from the csv files. (component_value, eufdname, food,
        saantisuositus)
    """

    component_value = pd.read_csv(path + "component_value_utf-8.csv", sep=";")
    eufdname = pd.read_csv(path + "eufdname_FI_utf-8.csv", sep=";")
    food = pd.read_csv(path + "food_utf-8.csv", sep=";")
    saantisuositus = pd.read_csv(path + "saantisuositus_2014.csv", sep=";", header=None, names=["EUFDNAME", "name", "mnuori", "maikuinen", "mkeski", "miäkäs", "mvanha", "npieni","nnuori", "naikuinen", "nkeski", "niäkäs", "nvanha"])

    return component_value, eufdname, food, saantisuositus

component_value, eufdname, food, saantisuositus = read_files('/home/pomo/Asiakirjat/Kurssit/Taitotalo_Python-ohjelmoija/python/portfolio/fineli_20/')

# ateriankorvikkeiden yms. poisto

def filter_food_class(dataframe:pd.DataFrame, class_to_remove:tuple, col:str='FUCLASS') -> pd.DataFrame:
    """Take a pandas dataframe with food data and remove
    lines where the FUCLASS is one of those specified in 
    fuclass_to_remove. Returns the cleaned dataframe.

    Args:
        dataframe (pandas_df): A pandas dataframe with food names and food classes (e.g. FUCLASS)
        class_to_remove (tuple): A tuple of food class names to use for filtering out unwanted data
        col (str): Column name, default = FUCLASS

    Returns:
        pandas_df: The pandas dataframe minus the lines with specified food class names
    """
    if col == 'FUCLASS':
        for food_class in class_to_remove:
            dataframe = dataframe[dataframe.FUCLASS != food_class]
    elif col == 'IGCLASS':
        for food_class in class_to_remove:
            dataframe = dataframe[dataframe.IGCLASS != food_class]
    else:
        raise ValueError(f'Invalid column name: {col}')

    return dataframe

# puuttuvien ravintoarvotietojen käsittely

def transpose_component_value(dataframe:pd.DataFrame) -> pd.DataFrame:
    """Takes a pandas dataframe (component_value) where each row represents
    the amount of one nutrient in one food (e.g. calcium in milk). 
    Transposes the dataframe so that there is one row per food and one column per nutrient.
    Fills in any missing component values with zeroes in the appropriate column.
    The ACQTYPE, METHTYPE, and METHIND columns are dropped.

    Args:
        dataframe (pandas_df): A pandas dataframe with information on how much of each nutrient foods contain

    Returns:
        pandas_df: The pandas dataframe modified so that it has one row per food and one column per nutrient.
    """
    df = dataframe.drop(columns=['ACQTYPE','METHTYPE', 'METHIND'])

    new_df = df.pivot_table(values='BESTLOC', index='FOODID', columns='EUFDNAME', fill_value=0.0)
    
    return new_df

