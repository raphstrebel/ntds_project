# NTDS Project

# Motivation
We want to limit food waste. Our approach is to propose receipes that maximize the number of ingredients that you have at home, while possibly minimizing the number of new ingredients you have to buy.

# Data Setup
We use the dataset "Cooking recipes". 
It contains the ingredients, the rating of the recipe (number of reviews and grade of the recipe to assign a popularity index), the cooking time, and for most of them we can estimate the upload year by looking at the earliest comment. 
Scraping will be needed since the dataset contains webpages, and it will take a long time since there are different types of webpages. 
We will then store the dataset into a pickle file in order to avoid to rerun the scraping part each time we open the notebook.

Cooking recipes dataset URL : http://infolab.stanford.edu/~west1/from-cookies-to-cooks/
Data : http://infolab.stanford.edu/~west1/from-cookies-to-cooks/recipePages.zip

We do not keep all the dataset, as it contains receipies from 163 websites. It would be simpler to build a graph using e.g. the 2 or 3 thousand first recipes.

# Setup

# Limitations
We do not have access to the quantity of an ingredient in a receipe, so we will use sets of ingredients without considering the weight/number of each of them.

# Graph 
As we use sets of ingredients, using the jaccard similarity as edge weighting method seems the most appropriate. 

# Goal
Recommending recipes using a list of available ingredients, and an unwanted ingredient list, which contains all the ingredients that the user does not wish for in the final recipes proposed.

# Authors
Elias Gajo, Karen Preitner, Raphael Strebel, Maël Wildi




