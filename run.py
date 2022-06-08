# python code goes here
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
SHEET = GSPREAD_CLIENT.open("love_sandwiches") # only smallcap allowed

# sales = SHEET.worksheet('sales')

# data = sales.get_all_values()

# print(data)

def get_sales_data():
    """ get sales figures from user """

    print('Plz enter sales data from the last market day')
    print('Data input in six numbers, separated by commas')
    print("Example: 6,5,4,3,2,1\n")

    data_str = input('Enter your data here: ')
    print(f'the data you send was {data_str}')

    sales_data = data_str.split(',')
    validate_data(sales_data)

def validate_data(values):
    """ validate input data from get_sales_data """
    print(values)
    try:
        if len(values) != 6:
            raise ValueError(
                f"expected six (6) number separated by comma (,) but {len(values) was given}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, plz do it again, becouse, if tomorrow never comes \n")

get_sales_data()