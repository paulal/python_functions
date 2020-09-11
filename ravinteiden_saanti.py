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

    # delete unwanted data
    for food_type in omitted_food_types:
        food = food[food.FUCLASS != food_type]
    
    return component_value, eufdname, food, saantisuositus

component_value, eufdname, food, saantisuositus = read_files('/home/pomo/Asiakirjat/Kurssit/Taitotalo_Python-ohjelmoija/python/portfolio/fineli_20/')
print(saantisuositus)