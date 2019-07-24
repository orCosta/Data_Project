#############################################################################################################
# Preprocessing
# This code crawling data about ingredients molecular structure from the website "foodb".
#############################################################################################################
from bs4 import BeautifulSoup
import requests
import numpy as np
import json
import pandas as pd

TOTAL_COMP = 31351
NUM_INGR = 419
COMP_DB = np.zeros((NUM_INGR, TOTAL_COMP))
f = open('ingredients.json')
ALL_FOOD_DICT = json.load(f)

def getFoodCompounds(item_id, item_idx):
    '''
    Crawl the data from 'foodb' website.
    :param item_id: The old/original id for the url.
    :param item_idx: The item's new index as it represent in the code.
    '''
    url = "http://foodb.ca/foods/" + str(item_id) + "/contents/dt_compound_index.all"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    text = soup.currentTag
    compList = str(text).split("compounds")
    num_comp = len(compList)-1
    for i in range(1, len(compList)):
        c_idx = compList[i][4:10]
        COMP_DB[item_idx, int(c_idx)] = 1
    print("found {0} compounds for item {1}".format(num_comp, item_id))

def initIngredientsCompoundsDB():
    '''
    This function crawls food compounds data from "foodb" website and store it in matrix s.t the rows represent the
    items and the columns represent the food compounds.
    :param item_list: list with the relevant items.
    :return: DB (matrix).
    '''
    all_data = pd.read_csv("rep_foods.csv", encoding='latin-1')
    requested_ings = list((all_data.values[:, 2]))
    for item in requested_ings:
        print(item)
        getFoodCompounds(ALL_FOOD_DICT[item][1], ALL_FOOD_DICT[item][0])
    return COMP_DB


# ################ MAIN ####################### #
print("Start crawling the data...")
initIngredientsCompoundsDB()
idx = np.argwhere(np.all(COMP_DB[..., :] == 0, axis=0))
db = np.delete(COMP_DB, idx, axis=1)
print("Save the DB...")
np.save("compdb.npy", db)
print("Finish the crawling")

