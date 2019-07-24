#############################################################################################################
# Preprocessing
# This code get the compounds DB and the ingredients shared histogram matrix and creates matrix of similarity
# between the replaceable ingredients.
#############################################################################################################
import numpy as np
import pandas as pd
import json

# #############################################################
# ################### LOAD ALL DB #############################
# Ingredients compounds matrix
compdb = np.load("compdb.npy").astype(np.int)
# Ingredients appearance histogram
f = open('ingredients.json')
ALL_FOOD_DICT = json.load(f)
TOTAL_ITEMS = len(ALL_FOOD_DICT)

id2name = {}
for key, val in ALL_FOOD_DICT.items():
    id2name[val[0]] = key

# List of all replaceable foods
all_data = pd.read_csv("rep_foods.csv", encoding='latin-1')
rep_ings = list((all_data.values[:, 2]))
# Shared appearance histogram (ingredients)
SHARED_HIST = pd.read_csv("ing_mat.csv", index_col=0, header=0)

# ##############################################################

def calc_BC_distance_for_ing(normalized, numIngs, index1):
    '''
    This function calculates the distance between ingredient x to all other ingredients.
    The calculation based on Bhattacharyya distance a way to measure similarity between probabilities.
    For more info : "https://en.wikipedia.org/wiki/Bhattacharyya_distance"
    '''
    if np.sum(normalized[:, index1]) == 0:
        return np.zeros(numIngs)
    dists = []
    for i in range(numIngs):
        if np.sum(normalized[:, i]) == 0:
            dists.append(np.inf)
        else:
            p = normalized[:, index1]
            q = normalized[:, i]
            dist = -np.log2(np.sum((p*q) ** .5))
            dists.append(min(dist, 1))
    dists[index1] = 1
    return np.array(dists)


def build_BC_sim_mat(normalized, numIngs):
    sim_mat = np.zeros((numIngs, numIngs))
    for i in range(numIngs):
        sim_mat[i] = calc_BC_distance_for_ing(normalized, numIngs, i)
    return sim_mat


def shared_hist_similarity_matrix():
    '''
    Builds similarity matrix between ingredients.
    return a matrix with the sizes (ALL_ING x ALL_ING) st row x contains the distance of ing x against all the others
    ingredients.
    The distance is between 0 to 1, (0- is the closest).
    The calculation based on probability of appearance, compere x to y we calculate the probability of item x of
    appearance with all other ingredients (based on recipes list) against the probability of item y to appearance with
    other ingredients.
    '''
    # Convert the shared hist matrix to probability matrix.
    hist = SHARED_HIST.as_matrix()
    np.fill_diagonal(hist, 0)

    numIngs = hist.shape[0]
    cols_sum = np.sum(hist, axis=0)
    normalized = np.divide(hist, cols_sum, out=np.zeros_like(hist), where=(cols_sum != 0))

    sim_mat = build_BC_sim_mat(normalized, numIngs)
    # Change the distance of ingredients that are not replaceable to 1.
    for id, item in id2name.items():
        if item in rep_ings:
            continue
        sim_mat[:, id] = 1
    # sim_mat = 1 - sim_mat
    return sim_mat


def food_compounds_similarity_matrix():
    '''
    Builds a similarity matrix with the sizes (ALL_ING x ALL_ING), in every cell x, y we can find the
    similarity between ing' x to ing' y. The similarity based on the molecular structure of the igredients.
    The ingredients compound db is binary so the similarity calculation based on JACCARD similarity.
    For more info: "https://en.wikipedia.org/wiki/Jaccard_index"
    '''
    sim_matrix = np.zeros((TOTAL_ITEMS, TOTAL_ITEMS))
    for item in rep_ings:
        item_idx = ALL_FOOD_DICT[item][0]
        scores_vec = np.dot(compdb, compdb[item_idx].T)
        if not scores_vec.any(): # pass over the ingredients without data
            sim_matrix[item_idx] = np.ones(len(scores_vec))
            # sim_matrix[item_idx][item_idx] = 0
            continue

        scores_vec[item_idx] = 0
        temp1 = np.bitwise_or(compdb, compdb[item_idx].T)
        scores_vec = scores_vec/(np.sum(temp1, axis=1))
        dist_vec = np.ones(len(scores_vec)) - scores_vec
        # dist_vec = dist_vec/ np.sum(dist_vec)
        sim_matrix[item_idx] = dist_vec
    return sim_matrix


def DEBUG_test(mat, item_idx, k):
    print("similarity for {}:".format(id2name[item_idx]))
    ind = np.argsort(mat[item_idx])[:k]
    vals = mat[item_idx][ind]
    for i in range(k):
        print("{}: similar item - {}, val is {}".format(i, id2name[ind[i]], vals[i]))
    print("***************************")


def main():
    '''
    Creates two similarity matrices and combine them to one.
    The matrix will save as "sim_matrix" numpy file.
    To run this code all the DB that are mentioned above are needed.
    '''
    sim_matrix1 = shared_hist_similarity_matrix()
    sim_matrix2 = food_compounds_similarity_matrix()
    a = 0.5
    b = 0.5
    f_sim_matrix = a * sim_matrix1 + b * sim_matrix2

    k = 10
    item = 3
    DEBUG_test(sim_matrix1, item, k)
    DEBUG_test(sim_matrix2, item, k)
    DEBUG_test(f_sim_matrix, item, k)

    np.save("sim_matrix.npy", f_sim_matrix)


if __name__ == '__main__':
    main()






