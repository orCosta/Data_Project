##############################################################################
# Histogram of compounds by ingredients categories
##############################################################################
import numpy as np
import pandas as pd
import json
from matplotlib import pyplot

f = open('ingredients.json')
ALL_FOOD_DICT = json.load(f)

id2name = {}
for key, val in ALL_FOOD_DICT.items():
    id2name[val[0]] = key

compdb = np.load("compdb.npy")

all_data = pd.read_csv("rep_foods.csv", encoding='latin-1')
items = list((all_data.values[:, 2]))

cat = list((all_data.values[:, 3]))
# cat_set = set(cat)
cat_set = {'Milk and milk products', 'Animal foods', 'Herbs and Spices'}
# cat_set = {'Animal foods', 'Pulses', 'Vegetables', 'Soy', 'Nuts', 'Fats and oils', 'Eggs', 'Herbs and Spices', 'Milk and milk products', 'Gourds', 'Cereals and cereal products', 'Beverages', 'Fruits'}
print(cat_set)
all_hist = {}
for c in cat_set:
    all_hist[c] = np.zeros(len(compdb[1]))

for i, item in enumerate(items):
    if cat[i] in cat_set:
        all_hist[cat[i]] += compdb[ALL_FOOD_DICT[item][0]]


bins = np.linspace(1, len(compdb[0]), len(compdb[0]))

for key, val in all_hist.items():
    pyplot.hist(val, bins, alpha=0.5, label=key)


# pyplot.hist(y, bins, alpha=0.5, label='y')
pyplot.legend(loc='upper right')
pyplot.title("Histogram compounds vs. food categories")
pyplot.show()

