# PROJECT CHEF

## Intro
This project generates recipes given 2-3 ingredients from the user. The generation is two fold - a basic search of existing recipes containing the user ingredients and creation of new recipes by replacing paired ingredients in existing recipes.

The pairing is mostly based on the hypothesis which states that ingredients sharing flavor compounds (chemical) are more likely to taste well together than ingredients that do not.
We also would like to pair ingredients from the same cateogry, for example, replacing fish fillet with chicken breast will be more suitable replacement than replacing fish fillet with brocolli.


Data Sets used:
Data set of ~420 general food products and their chemical structure:
Data set of 28K recipes:

Pre-Processing stage:
The ingredients in the recipes data set were given as free strings, and because our algorithm is based on switching
between ingredients, the process of normalizing them was necessary.
Normalizing the ingredients was done by running over all food products data set, creating a regex from them, and
checking each for every ingredient in every recipe

![‏‏לכידה](https://user-images.githubusercontent.com/44048156/61820008-ded16580-ae5c-11e9-8c3d-2141e6bcc433.JPG)

![2](https://user-images.githubusercontent.com/44048156/61818872-813c1980-ae5a-11e9-8a57-a49c2d984c18.JPG)
![4](https://user-images.githubusercontent.com/44048156/61818882-86996400-ae5a-11e9-9e04-802a170ece61.JPG)

## Similarity Graphs

![All_ing_1](https://user-images.githubusercontent.com/44048156/61819270-53a3a000-ae5b-11e9-9a41-dc8694a8265d.png)
![lemon_1](https://user-images.githubusercontent.com/44048156/61819271-53a3a000-ae5b-11e9-9d60-e0b799ccf79c.png)
![2‏‏לכידה](https://user-images.githubusercontent.com/44048156/61820009-ded16580-ae5c-11e9-9cc4-9e973b523869.JPG)
