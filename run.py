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
# only smallcap allowed on open filen
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


def get_sales_data():
    """ get sales figures from user """

    while True:
        print('Plz enter sales data from the last market day')
        print('Data input in six numbers, separated by commas')
        print("Example: 6,5,4,3,2,1\n")

        data_str = input('Enter your data here:\n')
        print(f'the data you send was {data_str}')

        sales_data = data_str.split(',')
        
        if validate_data(sales_data):
            print("data is valid")
            break
        
    return sales_data

def validate_data(values):
    """ validate input data from get_sales_data """
    print(values)
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"expected six (6) number separated by comma (,) but {len(values)} was given"
            )
    except ValueError as e:
        print(f"Invalid data: {e} \n")
        return False
    return True


def update_worksheet(data, worksheet):
    """ update google worksheet with sales, surplus & stocks """
    print(f"updating {worksheet} worksheet... \n ")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


def calculate_surplus_data(sales_row):
    """
    compare sales with stock:
    - negative indicates extra was made
    + plus indicates extra was given away to childe care
    """

    stock = SHEET.worksheet("stock").get_all_values()

    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_enteries_sales():
    """ get the last five days of sales statisitcs """

    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns


def calculate_stock_data(data):
    """ stock calculator based on five last sales """
    print("Calculating stock data..\n")

    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    
    return new_stock_data


def main():
    """ Run all program functions """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_enteries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")


print("Welcome to love sandwiches data automation")
main()