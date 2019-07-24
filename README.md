# PROJECT CHEF

## Intro
This project generates recipes given 2-3 ingredients from the user. The generation is two fold - a basic search of existing recipes containing the user ingredients and creation of new recipes by replacing paired ingredients in existing recipes.

The pairing is mostly based on the hypothesis which states that ingredients sharing flavor compounds (chemical) are more likely to taste well together than ingredients that do not.
We also would like to pair ingredients from the same cateogry, for example, replacing fish fillet with chicken breast will be more suitable replacement than replacing fish fillet with brocolli.


Data Sets used:
Data set of X general food products and their chemical(?) structure:
Data set of 28K recipes:

Pre-Processing stage:
The ingredients in the recipes data set were given as free strings, and because our algorithm is based on switching
between ingredients, the process of normalizing them was necessary.
Normalizing the ingredients was done by running over all food products data set, creating a regex from them, and
checking each for every ingredient in every recipe