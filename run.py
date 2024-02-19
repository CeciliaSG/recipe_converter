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

    print(user_choice)
    print(worksheet_titles)
    return user_choice in worksheet_titles

worksheet_titles = [worksheet.title.lower() for worksheet in SHEET.worksheets()]

user_choice = get_user_recipe_choice()
validate_user_recipe_choice(user_choice, worksheet_titles)


