import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint, pformat
from collections import ChainMap

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('recipe_converter')


def get_user_recipe_choice():
    """
    Gets the users's recipe choice.
    """
    print('Please choose a recipe from our recipe bank')
    #Display the recipes available to the user?
    user_choice = input('Please enter your choice: \n').lower()
    print(f'You chose {user_choice}\n')

    return user_choice 

def validate_user_recipe_choice(user_choice, worksheet_titles):
    """
    Checks if the user's recipe choice is in the recipe bank
    """
    while True:
        if user_choice in worksheet_titles:
              print(f"You have chosen {user_choice}. This recipe is available.")
              break
        else:
              print(f"Your choice: {user_choice}. No such recipe. Please choose recipe in our recipe bank.") 
              user_choice = input('Please enter your choice: ').lower()
    
    return user_choice          

worksheet_titles = [worksheet.title.lower() for worksheet in SHEET.worksheets()]
       
  
def get_required_portions():
    """
    Ask the user to input the required number of portions 
    for the recipe to use in calculation for ingredients amounts
    """
    while True:
        print('Enter number of portions for recipe: ')

        try:
            user_portions = int(input('Please enter number of portions: \n'))
            print(f'Portions: {user_portions}\n')

            if validate_user_portions(user_portions):
                print("Portions ✔")
                break

            else:
                print('Not a valid choice. Please try again')

        except ValueError:  
            print('Invalid input. Please enter a number.') 

    return user_portions

def validate_user_portions(value):
    """
    Validates the user_input for number of portions, 
    only one number allowed
    """
    try:
        value = int(value)
        if value < 1 or value > 100:
            raise ValueError(
                f"Choose a number between 1 and 100, you provided {value}"
            )
    except ValueError as e:   
        print(f"Not a correct choice: {e}")  
        return False

    return True

def input_request_metric_imperial(new_recipe, new_recipe_imperial):   

    """
    Lets the user chose if they want the measurements in imperial 
    or metric units, requires user to input correct answer
    """     
    while True:
        unit_choice = input('Please choose imperial/metric: \n')
        if unit_choice.lower() == 'metric':
                display_recipe_metric(new_recipe)
                break

        elif unit_choice.lower() == 'imperial':
                display_recipe_imperial(new_recipe_imperial)
                break

        else: 
                print('Please enter valid choice')

    return unit_choice        

  
def get_user_choice_ingredients(user_choice):

    """
    Access the ingredients for the user's chosen recipe 
    and returns the int or float values for calculation
    """
    ingredients = SHEET.worksheet(user_choice).get_all_values()

    ingredients_column = [row[2] for row in ingredients[1:]]
  
    return ingredients_column


def calculate_user_measurements(ingredients_column, user_portions):
    """
    Calculates the measurements with the users 
    chosen portions and recipe ingredients
    """

    ingredients_float = [float(ingredient) for ingredient in ingredients_column]
    new_measurements =  [round(ingredient * user_portions, 1) for ingredient in ingredients_float]

    return new_measurements

def display_recipe_new_measurements(user_choice, new_measurements):
    """
    Create the new recipe with the user's requested measurements, 
    and add the measurement labels and ingredient headings
    """
    data = SHEET.worksheet(user_choice).get_all_values()
    headings_column = [row[0] for row in data[1:]]

    metric_measurements = [row[1] for row in data[1:]]

    new_recipe = {heading: f"{measurement} {metric_measurements}" for heading, measurement, metric_measurements in zip(headings_column, new_measurements, metric_measurements)}  
    return new_recipe, metric_measurements


def convert_metrics_to_imperial_units(new_recipe, metric_measurements, user_choice):
    """
    Convert the new_recipe metric units to imperial 
    units. If there is litres, dl, grams or kg in the recipe, 
    convert to gallons, ounces, cups and pounds.

    1kg = 2.2046 pounds
    1gram = 0.03527 ounces
    1litre = 4.22675284 cups
    1dl = 0.422675284 cups
    """

    converted_measurements = []
    unconverted_measurements = []

    for heading, metric_measurements in new_recipe.items():
        conversion = False

        try:
            if 'gram' in metric_measurements:
                quantity = metric_measurements.split()[0]
                converted_measurement_ounces = round(float(quantity) * 0.03527, 1)
                converted_measurements.append(converted_measurement_ounces)
                conversion = True
                print("Converted_to_ounces:", converted_measurement_ounces, "ounces")
        except KeyError:
            pass        

        try:
            if 'dl' in metric_measurements:
                quantity = metric_measurements.split()[0]
                converted_measurement_dl_cups = round(float(quantity) * 0.422675284, 1)
                converted_measurements.append(converted_measurement_dl_cups)
                conversion = True
                print(converted_measurement_dl_cups, "cups")
        except KeyError:
            pass        
            
        try:    
            if 'kg' in metric_measurements:
                quantity = metric_measurements.split()[0]
                converted_measurement_pounds = round(float(quantity) * 2.2046, 1) 
                converted_measurements.append(converted_measurement_pounds)
                conversion = True
                print(converted_measurement_pounds, "pounds")
        except KeyError:
            pass        

        try:     
            if 'litres' in metric_measurements:
                quantity = metric_measurements.split()[0]
                converted_measurement_litres_cups = round(float(quantity) * 4.22675284, 1)
                converted_measurements.append(converted_measurement_litres_cups)
                conversion = True
                print(converted_measurement_litres_cups, "cups")    
        except KeyError:
            pass     

        if not conversion:
            unconverted_measurements.append((heading, metric_measurements)) 

    #print('converted:', converted_measurements)  

    data = SHEET.worksheet(user_choice).get_all_values()
    headings_column = [row[0] for row in data[1:]]
    imperial_measurements = [row[3] for row in data[1:]]

    new_recipe_imperial = {heading: f"{measurement} {converted_measurement}" for heading, measurement, converted_measurement in zip(headings_column, converted_measurements, imperial_measurements)}     
    unconverted_measurements = {heading: f"{measurement}" for heading, measurement in zip(headings_column, unconverted_measurements)}     

    new_recipe_imperial = ChainMap(new_recipe_imperial, unconverted_measurements) 
    print('New:', new_recipe_imperial)

    print('unconverted:', unconverted_measurements)
    #print('imperial:', new_recipe_imperial)
    return new_recipe_imperial

def display_recipe_metric(new_recipe):
    print(new_recipe)

def display_recipe_imperial(new_recipe_imperial):
    s = pformat(new_recipe_imperial)
    print('Recipe_imperial:', s)
    #print(new_recipe_imperial)

def main():

    while True:
    
        user_choice = get_user_recipe_choice()
        user_choice = validate_user_recipe_choice(user_choice, worksheet_titles)
        user_portions = get_required_portions()
        ingredients_column = get_user_choice_ingredients(user_choice)
        new_measurements = calculate_user_measurements(ingredients_column, user_portions)
        new_recipe, metric_measurements = display_recipe_new_measurements(user_choice, new_measurements)
        new_recipe_imperial = convert_metrics_to_imperial_units(new_recipe, metric_measurements, user_choice)
        unit_choice = input_request_metric_imperial(new_recipe, new_recipe_imperial)

        while True:
        
            user_choice_two = input('Do you want to cook something else? (yes/no) \n').lower()
            
            if user_choice_two == 'no':
                break

            elif user_choice_two == 'yes':
                break

            else:
                print('Invalid choice. Please enter yes or no')

        if user_choice_two == 'no':
            break

    print('Thank you for using our recipe converter.')
    

print('Welcome to our recipe bank, where you can convert each recipe \n for the exact number of portions you are cooking')
print('Recipes to choose from:\n')
main()
