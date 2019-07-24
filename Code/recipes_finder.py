import pandas as pd
import numpy as np
import json
import random
import time
import itertools
import os

RECIPES_NUM_TO_FIND = 5
SIMILAR_INGR_NUM = 3
NORMAL_TITLE = 2
INGS_LIST = 0
SIMILARITY_DICT = 1

MAX_RECIPES = 20
DEBUG = False
PRINT_RECIPES = True

def find_recipe_by_ingredients(ingr_list, num_to_find=RECIPES_NUM_TO_FIND):
    '''
    :param ingr_list: list of ingredients
    :param num_to_find: number of recipes to find
    :return: list of recipes containing all given ingredients
    '''
    matched_recipes = []
    # for recipes_dict in all_recipes:
    for title, recipe in all_recipes.items():
        recipe_ingr = recipe['Recognized Ingredients']
        if set(ingr_list).issubset(recipe_ingr):
            title = title.split(':')[0][:-7] # remove irrelevant data
            matched_recipes.append((title, recipe['Link']))
            if len(matched_recipes) == num_to_find:
                break
    return matched_recipes

def find_most_similar_ingr(ingredient):
    ''' this function receives an ingredient and find its most similar ingredients
    :param ingredient: list of ingredients
    :return: [list of similar ingredients, ingredient to similarity dict]
    '''
    ingr_idx = ing2index[ingredient][0]
    ingr_similarities = similarity_mat[ingr_idx]
    most_similar_idx = ingr_similarities.argsort()[:SIMILAR_INGR_NUM]
    similar_ingredients = [all_ings[index][NORMAL_TITLE] for index in most_similar_idx] #list of all similar ingredients
    # dict of ingredient to similarity
    ingr_to_similarity = {all_ings[index][NORMAL_TITLE] : similarity_mat[ingr_idx][index] for index in most_similar_idx}
    if DEBUG:
        print("Original Item: ", ingredient)
        for ing in similar_ingredients:
            print("Similar item: {}".format(ing))
            print("similarity: ", ingr_to_similarity[ing])
        print("_______________________________________________")
    return [similar_ingredients, ingr_to_similarity]


def find_all_ings_permutations(ingredients_list, similar_ings):
    '''
    :param ings_list: list of input ingredients
    :return: list of all possible similar ingredients permutations, sorted by total similarity
    '''
    ingredients_options = [[ingredient] + similar_ings[ingredient][INGS_LIST] for ingredient in ingredients_list]
    all_permutations = list(itertools.product(*ingredients_options))
    return all_permutations


def get_total_similarity(orig_ings, ings_permutation, similar_ings, similarity_mat):
    '''
    :param orig_ings: original input ingredients
    :param ings_permutation: permutation of original ingredients & their similar ingredients
    :param similar_ings: dict of ingredient : [similar_ingredients_list, ing_to_similarity]
    :param similarity_mat: similarity matrix of all_ings X all_ings
    :return: total similarity score of the given ingredients permutation
    '''
    similarity = 0
    for i,ingredient in enumerate(ings_permutation):
        if ingredient in orig_ings:
            similarity += 0
        else:
            original_ing = orig_ings[i]
            original_ing_idx = ing2index[original_ing][0]
            # similarity_dict = similar_ings[original_ing][SIMILARITY_DICT]
            # similarity += similarity_dict[ingredient]
            ingredient_idx = ing2index[ingredient][0]
            similarity += similarity_mat[original_ing_idx][ingredient_idx]
    return similarity

def suggest_recipes(input_ingredients):
    '''
    :param input_ingredients: input ingredients given by the user
    :return: list of suggested recipes
    '''
    recipes = []

    all_similar_ingredients = {}
    for ingredient in input_ingredients:
        all_similar_ingredients[ingredient] = find_most_similar_ingr(ingredient)

    # Next rows find all possible permutations of input ingredients & their similar items, and sort them by total
    # similarity
    all_ings_permutations = find_all_ings_permutations(input_ingredients,all_similar_ingredients)
    get_similarity = lambda permutation : get_total_similarity(input_ingredients, permutation,
                                                               all_similar_ingredients, similarity_mat)
    all_ings_permutations.sort(key=get_similarity) # sort all permutations by similarity to original ings
    if DEBUG:
        for permut in all_ings_permutations:
            print(permut)
            print(get_total_similarity(input_ingredients, permut, all_similar_ingredients, similarity_mat))
            print("___________________________________________________")

    for permutation in all_ings_permutations:
        if len(permutation) != len(set(permutation)): # avoids duplicates in inputs similar ingredients
            continue
        new_recipes = find_recipe_by_ingredients(permutation)
        if new_recipes:
            recipes += [("Recipe #{}: {}\n{}URL: ".format(len(recipes) + i + 1, recipe[0], get_substitution_label(
                permutation, input_ingredients)), recipe[1]) for i,recipe in enumerate(new_recipes)]

        if len(recipes) > MAX_RECIPES:
            break

    if PRINT_RECIPES:
        for recipe in recipes:
            print(recipe[0])
            print(recipe[1], '\n')
    return recipes if recipes else [("There were no results found :(", "")]

def get_substitution_label(ingredients, input_ingredients):
    '''
    returns the label of ingredients substitutions for
    :param ingredients: ingredients used in a recipe
    :param input_ingredients: original ingredients as received by the user
    :return: label which indicates which ingredient is used in a recipe and which need to be substituted
    '''
    label = ''
    for i,ingredient in enumerate(ingredients):
        label += 'Use your {}\n'.format(ingredient) if ingredient in input_ingredients else\
            'Use {} instead of {}\n'.format(input_ingredients[i], ingredient)
    return label

def load_all_recipes():
    '''
    loads all recipes json files into a single recipes dict
    :return: all recipes dict
    '''
    json_dir = '../Data/full_preprocessing_stage2/recipes/'
    json_files = os.listdir(json_dir)
    recipes = {}
    for recipes_file in json_files:
        full_dir = json_dir + recipes_file
        # To avoid any crashes
        try:
            new_recipes = json.load(open(full_dir))
            recipes.update(new_recipes)
        except:
            continue
    return recipes


similarity_mat = np.load('../Data/sim_matrix.npy')
ing2index = json.load(open('../Data/full_preprocessing_stage2/ingredients.json'))

all_recipes = load_all_recipes()
all_ings = pd.read_csv('../Data/New Data/new_foods.csv', encoding='latin-1').values

ings_selection = pd.read_csv('../Data/New Data/new_foods_short.csv', encoding='latin-1').values

input_ingredients = np.random.choice(ings_selection[:, 2], 3)
# input_ingredients = ['strawberr', 'chicken', 'oregano']
print("Input Ingredients: ", input_ingredients)
result = suggest_recipes(input_ingredients)


