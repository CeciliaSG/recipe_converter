# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
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
    #How to display the recipes available to the user
    data_str = input('Please enter your choice: ')
    print(f'You choose {data_str}\n')

    return data_str

get_user_recipe_choice()   