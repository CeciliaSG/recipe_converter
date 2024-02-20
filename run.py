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
print("Worksheet Titles:", worksheet_titles)


def get_required_portions():
    """
    Ask the user to input the required number of portions for the recipe to use in calculation for ingredients amounts
    """
    while True:
        print('Enter number of portions for recipe: ')
        user_portions = input('Please enter number of portions: ')
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

  
def get_user_choice_ingredients():

    ingredients = SHEET.worksheet('Butter chicken').get_all_values()
    print(ingredients)


def main():

    user_choice = get_user_recipe_choice()
    validate_user_recipe_choice(user_choice, worksheet_titles)
    user_portions = get_required_portions()
    get_user_choice_ingredients()
    

print('Welcome to our recipe bank, where you can  convert each recipe for the exact number of portions you are cooking')
main()



