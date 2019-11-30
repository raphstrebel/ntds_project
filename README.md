# NTDS Project

# Motivation

# Getting data

# Understanding the data

# Using data
- find recipes from list of ingredients
- replace non-vegetarian ingredients (?)

# Data Setup

We plan to use the dataset "Cooking recipes". 
It contains the ingredients, the rating of the recipe (number of reviews and grade of the recipe to assign a popularity index), the cooking time, and for most of them we can estimate the upload year by looking at the earliest comment. 
Scraping will be needed since the dataset contains webpages, and it will take a long time since there are different types of webpages. 
We will then store the dataset into a pickle file in order to avoid to rerun the scraping part each time we open the notebook.

Cooking recipes dataset URL : http://infolab.stanford.edu/~west1/from-cookies-to-cooks/recipePages.zip

# Authors
Elias Gajo, Karen Preitner, Raphael Strebel, Maël Wildi
