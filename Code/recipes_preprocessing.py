import json
import re
import os
import pandas as pd
import numpy as np
import time


def normalize_ingredients(recipe, foods):
    '''
    this function receives a recipe, and normalize its ingredients by matching regex of all food products
    :param recipe: recipe to normalize
    :param foods: list of all food products
    :return: list of normalized ingredients
    '''
    normal_ingr = set()
    missed_ingrd = 0
    with open("preprocessing_log.txt", "a") as file:
        file.write("\n_____________________________________________________________")
    for ingredient in recipe['ingredientLines']:
        found = False
        for optional_ing in all_ings:
            regex = re.compile(".*" + optional_ing + ".*") # create a regex of food product
            if regex.match(ingredient.lower()):
                normal_ingr.add(optional_ing)
                found = True
                break
        if not found:
            with open("preprocessing_log.txt", "a") as file:
                file.write("\nThe next ingredient wasn't found: " + ingredient) # log missed ingredients
            missed_ingrd += 1

    if missed_ingrd :
        with open("preprocessing_log.txt", "a") as file:
            file.write("\nmissed {} ingredients".format(missed_ingrd))

    normal_ingr = list(normal_ingr)
    count_joint_appearances(normal_ingr)

    # count all ingredients' appearances
    for ingredient in normal_ingr:
        ings[ingredient][2] += 1  # increase ingredient's counter by 1

    with open("preprocessing_log.txt", "a") as file:
        file.write("\n" + str(normal_ingr))
        file.write("\n" + str(recipe['ingredientLines']))
    return normal_ingr

def count_joint_appearances(recipe_ingredients):
    '''
    counts all joint appearances of 2 ingredients in a recipe, updates matrix accordingly
    :param ingredients:
    :return:
    '''
    for ingr1 in range(len(recipe_ingredients)):
        for ingr2 in range(ingr1, len(recipe_ingredients)):
            a = ings[recipe_ingredients[ingr1]][0]
            b = ings[recipe_ingredients[ingr2]][0]
            joint_appearances[a][b] += 1
            #  prevents double counting of main diagonal
            if a != b:
                joint_appearances[b][a] += 1


if __name__ == '__main__':
    start = time.time()

    all_ings = pd.read_csv('../Data/New Data/new_foods.csv', encoding='latin-1')

    # dictionary of ingredients as keys, values are list of [ingredient_index, ingredient id, ingredient_counter]
    ings = {norm_name: [i, id, 0] for (i, (id, _, norm_name)) in enumerate(all_ings.values[:, :3])}

    # create a list of all ingredients normalized tokens, sorted by len in descending order
    all_ings = list((all_ings.values[:, 2]))
    all_ings.sort(key=len, reverse=True)

    ALL_INGS_NUM = len(all_ings)
    joint_appearances = np.zeros((ALL_INGS_NUM, ALL_INGS_NUM))
    skipped = 0
    total_ing = 0
    recognized_ing = 0
    recipes_dict = dict()

    json_dir = '../Data/metadata27638/'
    json_index = 1

    with open("../Data/full_preprocessing_stage2/preprocessing_log_updated.txt", "w") as file:
        file.write("####### PREPROCSSING LOG #######\n")

    json_files = os.listdir(json_dir)
    for i, recipe_file in enumerate(json_files):
        # if i == 1000:
        #     break

        full_dir = json_dir + recipe_file

        # To avoid any crashes
        try:
            recipe = json.load(open(full_dir))
        except:
            skipped += 1
            continue

        # Finds normalized names:
        norm_ings = normalize_ingredients(recipe, all_ings)
        recognized_ing += len(norm_ings)
        total_ing += len(set(recipe['ingredientLines']))

        # Builds shorter dict for better recipes and ingredients research
        recipes_dict[recipe['attribution']['text']] = {
            'Original Ingredients': recipe['ingredientLines'],
            'Recognized Ingredients': norm_ings,
            'Cuisine': recipe['attributes']['cuisine'],
            'Link': recipe['attribution']['url']
        }
        # Saves new json file each 5000 iterations & on final iteration
        if ((i and i % 5000 == 0) or i == len(json_files) - 1):
            with open('../Data/full_preprocessing_stage2/recipes/recipes_short_' + str(json_index)+ '.json', 'w') as fp:
                json.dump(recipes_dict, fp)
            recipes_dict = dict()
            print("Created Json file num: {} in {} minutes".format(json_index, (time.time() - start) / 60))
            json_index += 1

    # saves matrix of joint appearances
    pd.DataFrame(joint_appearances).to_csv("../Data/full_preprocessing_stage2/ing_mat.csv")
    # saves dictionary of ingredients
    with open('../Data/full_preprocessing_stage2/ingredients.json', 'w') as fp:
        json.dump(ings, fp)

    with open("preprocessing_log.txt", "a") as file:
        file.write("\nRecipes skipped: " + str(skipped))
        file.write("\nTotal Ingredients, " + str(total_ing))
        file.write("\nRecognized Ingredients, " + str(recognized_ing))
        end = time.time()
        file.write("\nPreprocessing took: {} minutes".format ((end - start) / 60))
    end = time.time()
    print("Finished Pre-processing in {} minutes".format ((end - start) / 60))
