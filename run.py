import gspread
from google.oauth2.service_account import Credentials

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
    Gets the users's recipe choice
    """
    print('Please choose a recipe from our recipe bank')
    #Display the recipes available to the user?
    user_choice = input('Please enter your choice: ').lower()
    print(f'You chose {user_choice}\n')

    return user_choice 

def validate_user_recipe_choice(user_choice, worksheet_titles):
    """
    Checks if the user's recipe choice is in the recipe bank
    """

    #user_choice = f"'{user_choice}'"
    #return user_choice in worksheet_titles

    if user_choice in worksheet_titles:
              print(f"You have chosen {user_choice}. This recipe is available.")
    else:
              print(f"Your choice: {user_choice}. No such recipe. Please choose recipe in our recipe bank.") 

worksheet_titles = [worksheet.title.lower() for worksheet in SHEET.worksheets()]

def get_required_portions():
    """
    Ask the user to input the required number of portions for the recipe to use in calculation for ingredients amounts
    """
    while True:
        print('Enter number of portions for recipe: ')
        user_portions = int(input('Please enter number of portions: '))
        print(f'Portions: {user_portions}\n')

        if validate_user_portions(user_portions):
            print("Portions are ok")
            break

    return user_portions

def validate_user_portions(value):
    """
    Validates the user_input for number of portions, only one number allowed
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

  
def get_user_choice_ingredients(user_choice):

    """
    Access the ingredients for the user's chosen recipe and returns the integer values for calculation
    """
    ingredients = SHEET.worksheet(user_choice).get_all_values()

    ingredients_column = [row[2] for row in ingredients[1:]]
  
    return ingredients_column

def calculate_user_measurements(ingredients_column, user_portions):
    """
    Calculates the measurements with the users chose portions and recipe ingredients
    """

    ingredients_float = [float(ingredient) for ingredient in ingredients_column]
    new_measurements =  [ingredient * user_portions for ingredient in ingredients_float]

    return new_measurements

def print_recipe_new_measurements(user_choice, new_measurements):
    """
    Create the new recipe and display to the user
    """

    headings = SHEET.worksheet(user_choice).get_all_values()
    headings_column = [row[0] for row in headings[1:]]

    new_recipe = {headings: measurement for headings, measurement in zip(headings_column, new_measurements)}
    
    print('new recipe:', new_recipe)    
    return new_recipe

def convert_metrics_to_imperial_units():

    metrics = SHEET.worksheet(user_choice).get_all_values()
    metric_measurements = [row[1] for row in metrics[1:]]


 


def main():

    user_choice = get_user_recipe_choice()
    validate_user_recipe_choice(user_choice, worksheet_titles)
    user_portions = get_required_portions()
    ingredients_column = get_user_choice_ingredients(user_choice)
    new_measurements = calculate_user_measurements(ingredients_column, user_portions)
    new_recipe = print_recipe_new_measurements(user_choice, new_measurements)
    

print('Welcome to our recipe bank, where you can  convert each recipe for the exact number of portions you are cooking')
main()



