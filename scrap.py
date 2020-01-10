from pathlib import Path
import shutil
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import numpy as np


def try_reading(filename, max_iter = 3):
    result= None
    i = 0
    while (result is None) or i <= max_iter:
        i+=1
        try:
            result = BeautifulSoup(open(filename), "html.parser") 
        except:
            print("Error Reading")
            pass
    return result

##################### SCRAPING FUNCTIONS
def scrap_allrecipes(website, filename, list_ingredient_to_remove, list_unique_ingredients, recipe_data, website_list_used ,unique_ingredients_data):
                                                                                                # used_0 correspond to the first website i.e allrecipes
    try:
        soup = BeautifulSoup(open(filename), "html.parser")
    except:
        print("Beautifulsoup can't read the page:",filename)
        return recipe_data, list_unique_ingredients, unique_ingredients_data
                
    recipe_name = soup.find('span', class_='itemreviewed')
                
    #We only take recipes and not searching pages
    if recipe_name is None:
        print("We don't care about this page: ",filename)
        return recipe_data, list_unique_ingredients, unique_ingredients_data
        
    recipe_name = recipe_name.text
    
    rating_html = soup.find('img', class_='rating')
                
    #Determine position of the ranking in the string
    start_rank = 59
    end_rank = 62
    rating = rating_html['title'][start_rank:end_rank]
          
    #print(recipe_name)
    #print(rating)
                
    #Determine the number of reviews:
    if soup.find('span', class_='count') is not None:
        review_html = soup.find('span', class_='count').text
        review = int(review_html.replace(',',''))
    else:
        review = 0
        #print('Reviews :',review)
    
    #Find the preparation time:
    prepare_time = np.nan
    soup1 = soup.find('span', class_='totalTime')
    if soup1 is not None:
                
        prepare_time_html = soup1.find('span', class_='value-title')
        #Determine position of the time in the string
        start_prepare_time = 2
        end_prepare_time = len(prepare_time_html['title']) 
        prepare_time_not_converted = prepare_time_html['title'][start_prepare_time:end_prepare_time]
        #print("prepare time", prepare_time_not_converted)
        #If recipe is more than a day:
        if ('Day' or 'Days') in prepare_time_not_converted:
            text_to_split_on ="" 
            if 'Days' in prepare_time_not_converted:
                text_to_split_on = 'Days' 
            else:
                text_to_split_on = 'Day'
            time_analyse = prepare_time_not_converted.split(text_to_split_on)
            time_hours = time_analyse[1].split('H')
            #To convert into minutes (add the days and hours to the minutes)
            if len(time_hours) == 1:
                try:
                    prepare_time = int(time_analyse[0])*60*24 + int(time_hours[0].replace('M',''))
                except:
                    print("text time", time_analyse, " filename", filename)
                    return recipe_data, list_unique_ingredients, unique_ingredients_data
            if len(time_hours) == 2:
                time_minute = time_hours[1].replace('M','');
                prepare_time = int(time_analyse[0])*60*24 + int(time_hours[0])*60 + (int(time_minute) if time_minute else 0) 
             #If the recipe is only in hours and minutes        
        else:
            time_analyse = prepare_time_not_converted.split('H')
            #To convert hours into minutes
            if len(time_analyse) == 1:
                prepare_time = int(time_analyse[0].replace('M',''))
            if len(time_analyse) == 2:
                time_minute = time_analyse[1].replace('M','');
                prepare_time = int(time_analyse[0])*60 + (int(time_minute) if time_minute else 0)
                    
                
    #Find the ingredient list:
    list_ingred = []
    ingredients = soup.find('div', class_='ingredients')
    
    if ingredients is None:
        print("No ingredients found :", filename)
        return recipe_data,list_unique_ingredients, unique_ingredients_data
    
    all_ingredients = ingredients.find_all('li',class_="plaincharacterwrap ingredient")
    for ingredient in all_ingredients:
        ingredient_i = ingredient.text.replace('\n','').lower()
        #print('Original:', ingredient_i)
        ingredient_i = ingredient_i.split(',')[0]
        ingredient_i = [word for word in ingredient_i.split(' ') if word not in list_ingredient_to_remove] #Clean string to only have the ingredient
        ingredient_i = ' '.join(x for x in ingredient_i if x.isalpha()) + ' '
        ingredient_i = ingredient_i.replace(' or ', '//').replace(' and ','//').replace(' with ','//').split('//') #if options, add both in the list
        #print('After removing:              ', ingredient_i,"\n")
                    
        for ingredient_in_list in ingredient_i:
            ingredient_in_list_strip = ingredient_in_list.strip()                        
            if ingredient_in_list_strip == '':
                continue
            if ingredient_in_list_strip[len(ingredient_in_list_strip)-1] == 's' and ingredient_in_list_strip[0:len(ingredient_in_list_strip)-1] in list_unique_ingredients:
                ingredient_in_list_strip = ingredient_in_list_strip[0:len(ingredient_in_list_strip)-1] #Remove the plural form (s) of the ingredient
                    
            list_ingred.append(ingredient_in_list_strip) #Add the element to the ingredient list  
            if ingredient_in_list_strip not in list_unique_ingredients:
                list_unique_ingredients.append(ingredient_in_list_strip)
#                 print("list unique ingredient", list_unique_ingredients)
                unique_ingredients_data = unique_ingredients_data.append({'Ingredient': ingredient_in_list_strip, 'Count': 1}, ignore_index=True)
            #If ingredient already seen, increment the count of it
            else:
                ingredient_index = unique_ingredients_data[unique_ingredients_data['Ingredient']== ingredient_in_list_strip].index[0]
                unique_ingredients_data.at[ingredient_index,'Count'] = unique_ingredients_data['Count'][ingredient_index] + 1
                            
                    
            #print(list_ingred) 
            
    recipe_data = recipe_data.append({'Website': website, 'Recipe': recipe_name,'Prepare time': prepare_time, 'Ranking': rating, 'Reviews': review,\
                                                  'Ingredients': list_ingred}, ignore_index=True)
    return recipe_data, list_unique_ingredients, unique_ingredients_data

## Scraping the files of the domain food.com
#def scrap_food(website, filename, list_ingredient_to_remove, list_unique_ingredients, recipe_data, website_list_used ,unique_ingredients_data):
def scrap_food(website, filename,list_ingredient_to_remove, \
                                            list_unique_ingredients, recipe_data,website_list_used,unique_ingredients_data):                                                                                             
    try:
        soup = BeautifulSoup(open(filename), "html.parser")
    except:
        print("Beautifulsoup can't read the page (food.com):",filename)
        return recipe_data, list_unique_ingredients, unique_ingredients_data
#     soup = try_reading(filename)
#     if soup is None:
#         print("Beautifulsoup can't read the page (food.com):",filename)
#         return recipe_data, list_unique_ingredients, unique_ingredients_data
                
    recipe_name = soup.find('h1', class_='fn')
                
    #We only take recipes and not searching pages
    if recipe_name is None:
        print("No name found : We don't care about this page: ",filename)
        return recipe_data, list_unique_ingredients, unique_ingredients_data
        
    recipe_name = recipe_name.text
    
    rating = soup.find('li', {"class":"current-rating"})
    # If no rating can be found, we don't use the file
    if rating is None:
        print("No rating found")
        return recipe_data, list_unique_ingredients, unique_ingredients_data
    rating = float(rating["style"][7:-2]) *5/100 # the review is a percentage of 5 stars storred in the attribute of a li block
    #print("rating", rating)   
    #print(recipe_name)
    #print(rating)
    if recipe_name is None:
        print("No name but rating found at the file ", filename)
    #Determine the number of reviews:
    review_html = soup.find('span', itemprop='reviewCount')
    if review_html is not None:
        review = int(review_html.text.replace(',',''))
    else:
        review = 0
    
    #Find the preparation time:
    prepare_time = np.nan
    soup1 = soup.find('h3', class_='duration')
    if soup1 is not None:
        
        words_time = soup1.text.strip().split(" ")
        len_words_time = len(words_time)
        if len_words_time %2 == 1:
            print("strange words", words_time)
        
        prepare_time = 0
        for i in range(int(len_words_time/2)):
            try : 
                prepare_time += 60**i * int(words_time[len_words_time -(1+i)*2])
            except :
                prepare_time = 0 
                print(" ERROR TIME on file ", filename, " with time ", words_time, "and text", soup1.text)            
                
    #Find the ingredient list:
    list_ingred = []
    ingredients = soup.find('div', class_='pod ingredients')
    
    if ingredients is None:
        print("No ingredients found :", filename)
        return recipe_data,list_unique_ingredients, unique_ingredients_data
    
    all_ingredients = ingredients.find_all('a')
    for ingredient in all_ingredients:
        ingredient_i = ingredient.text.replace('\n','').lower()
        #print('Original:', ingredient_i)
        ingredient_i = ingredient_i.split(',')[0]
        ingredient_i = [word for word in ingredient_i.split(' ') if word not in list_ingredient_to_remove] #Clean string to only have the ingredient
        ingredient_i = ' '.join(x for x in ingredient_i if x.isalpha()) + ' '
        ingredient_i = ingredient_i.replace(' or ', '//').replace(' and ','//').replace(' with ','//').split('//') #if options, add both in the list
        #print('After removing:              ', ingredient_i,"\n")
                    
        for ingredient_in_list in ingredient_i:
            ingredient_in_list_strip = ingredient_in_list.strip()                        
            if ingredient_in_list_strip == '':
                continue
            if ingredient_in_list_strip[len(ingredient_in_list_strip)-1] == 's' and ingredient_in_list_strip[0:len(ingredient_in_list_strip)-1] in list_unique_ingredients:
                ingredient_in_list_strip = ingredient_in_list_strip[0:len(ingredient_in_list_strip)-1] #Remove the plural form (s) of the ingredient
                    
            list_ingred.append(ingredient_in_list_strip) #Add the element to the ingredient list  
            
            if ingredient_in_list_strip not in list_unique_ingredients:
                list_unique_ingredients.append(ingredient_in_list_strip)
#                 print("list unique ingredient", list_unique_ingredients)
                unique_ingredients_data = unique_ingredients_data.append({'Ingredient': ingredient_in_list_strip, 'Count': 1}, ignore_index=True)
            #If ingredient already seen, increment the count of it
            else:
                ingredient_index = unique_ingredients_data[unique_ingredients_data['Ingredient']== ingredient_in_list_strip].index[0]
                unique_ingredients_data.at[ingredient_index,'Count'] = unique_ingredients_data['Count'][ingredient_index] + 1
                    
            #print(list_ingred) 
            
    recipe_data = recipe_data.append({'Website': website, 'Recipe': recipe_name,'Prepare time': prepare_time, 'Ranking': rating, 'Reviews': review,\
                                                  'Ingredients': list_ingred}, ignore_index=True)
    return recipe_data,list_unique_ingredients, unique_ingredients_data

#Scrap foodnetwork
def scrap_foodnetwork(website, filename, list_ingredient_to_remove, list_unique_ingredients, recipe_data, website_list_used ,unique_ingredients_data):
    #print('The file is a foodnetwork:', filename)                                                                                   # used_2 correspond to the first website i.e foodnetwork
    try:
        soup = BeautifulSoup(open(filename), "html.parser")
    except:
        print("Beautifulsoup can't read the page (foodnetwork):",filename)
        return recipe_data,list_unique_ingredients, unique_ingredients_data
                
    recipe_name = soup.find('h1', class_='fn')
                
    #We only take recipes and not searching pages
    if recipe_name is None:
        print("We don't care about this page (foodnetwork): ",filename)
        return recipe_data,list_unique_ingredients, unique_ingredients_data
        
    recipe_name = recipe_name.text
    
    #print("the recipe_name is :",recipe_name)
    
    rating_html = soup.find('div', class_='rm-block lead hreview-aggregate review')
    if (rating_html is None) or (rating_html.find('div') is None):
        print("No rating found")
        return recipe_data, list_unique_ingredients, unique_ingredients_data 
    
    #Determine the rating in the html sequence
    rating = rating_html.find('div')['title']
    #rating =  rating_html.find('div')['title']
          
    #print("the rating is:", rating)
                
    #Determine the number of reviews:
    review = 0
    if soup.find('div', class_='rm-block lead hreview-aggregate review') is not None:
        review_html = soup.find('li', class_='cta count')
        review = review_html.find('a').text
        review = [int(s) for s in review.split() if s.isdigit()]
        review = int(review[0])
    else:
        review = 0
        
    #print('The number of Reviews:',review)
    
    #Find the preparation time:
    prepare_time = np.nan
    prepare_time_html = soup.find('span', class_='value-title rspec-value-small')
    if prepare_time_html is not None:
                
        prepare_time_not_converted = prepare_time_html['title'].replace('PT','')
        
        #If recipe is more than a day:
        if ('Day' or 'Days') in prepare_time_not_converted:
            text_to_split_on ="" 
            if 'Days' in prepare_time_not_converted:
                text_to_split_on = 'Days' 
            else:
                text_to_split_on = 'Day'
            time_analyse = prepare_time_not_converted.split(text_to_split_on)
            time_hours = time_analyse[1].split('H')
            #To convert into minutes (add the days and hours to the minutes)
            if len(time_hours) == 1:
                prepare_time = int(time_analyse[0])*60*24 + int(time_hours[0].replace('M',''))
            if len(time_hours) == 2:
                time_minute = time_hours[1].replace('M','');
                prepare_time = int(time_analyse[0])*60*24 + int(time_hours[0])*60 + (int(time_minute) if time_minute else 0) 
             #If the recipe is only in hours and minutes        
        else:
            time_analyse = prepare_time_not_converted.split('H')
            #To convert hours into minutes
            if len(time_analyse) == 1:
                prepare_time = int(time_analyse[0].replace('M',''))
            if len(time_analyse) == 2:
                time_minute = time_analyse[1].replace('M','');
                prepare_time = int(time_analyse[0])*60 + (int(time_minute) if time_minute else 0)
                    
    #print('The time is:',prepare_time )           
    #Find the ingredient list:
    list_ingred = []
    ingredients = soup.find('ul', class_='kv-ingred-list1')
    if ingredients is None:
        ingredients = soup.find('ul', class_='kv-ingred-list2')  
        
    if ingredients is None:
        print("No ingredients found :", filename)
        return recipe_data,list_unique_ingredients, unique_ingredients_data
        
    all_ingredients = ingredients.find_all('li',class_="ingredient")
    for ingredient in all_ingredients:
        ingredient_i = ingredient.text.replace('\n','').lower()
        #print('Original:', ingredient_i)
        ingredient_i = ingredient_i.split(',')[0]
        ingredient_i = [word for word in ingredient_i.split(' ') if word not in list_ingredient_to_remove] #Clean string to only have the ingredient
        ingredient_i = ' '.join(x for x in ingredient_i if x.isalpha()) + ' '
        ingredient_i = ingredient_i.replace(' or ', '//').replace(' and ','//').replace(' with ','//').split('//') #if options, add both in the list
        #print('After removing:              ', ingredient_i,"\n")
                    
        for ingredient_in_list in ingredient_i:
            ingredient_in_list_strip = ingredient_in_list.strip()                        
            if ingredient_in_list_strip == '':
                continue
            if ingredient_in_list_strip[len(ingredient_in_list_strip)-1] == 's' and ingredient_in_list_strip[0:len(ingredient_in_list_strip)-1] in list_unique_ingredients:
                ingredient_in_list_strip = ingredient_in_list_strip[0:len(ingredient_in_list_strip)-1] #Remove the plural form (s) of the ingredient
                    
            list_ingred.append(ingredient_in_list_strip) #Add the element to the ingredient list  
            if ingredient_in_list_strip not in list_unique_ingredients:
                list_unique_ingredients.append(ingredient_in_list_strip)
#                 print("list unique ingredient", list_unique_ingredients)
                unique_ingredients_data = unique_ingredients_data.append({'Ingredient': ingredient_in_list_strip, 'Count': 1}, ignore_index=True)
            #If ingredient already seen, increment the count of it
            else:
                ingredient_index = unique_ingredients_data[unique_ingredients_data['Ingredient']== ingredient_in_list_strip].index[0]
                unique_ingredients_data.at[ingredient_index,'Count'] = unique_ingredients_data['Count'][ingredient_index] + 1
                            
                    
            
    #print(list_ingred)        
    recipe_data = recipe_data.append({'Website': website, 'Recipe': recipe_name, 'Prepare time': prepare_time, 'Ranking': rating, 'Reviews': review,\
                                                  'Ingredients': list_ingred}, ignore_index=True)
    return recipe_data,list_unique_ingredients, unique_ingredients_data

