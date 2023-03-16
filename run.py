"""
Import libraries
"""
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('garden-bar-stock')


def get_entries_data():
    """
    Get entries input from the user.
    Running a while loop that should recive
    valide input from the user, the loop
    should be repeted until the input is valid.
    The input should contain a string
    of 5 numbers separated by a comma
    that can be divisible by 6
    """
    while True:
        print("Please enter the number of bottles "
              "for each drink introduced in the bar.")
        print("Data should be 5 numbers divisible by 6, "
              "separated by commas.")
        print("Example: 12,24,36,48,60\n")

        entries_str = input("Enter the number of bottles here: ")

        entries_data = entries_str.split(",")

        if validate_entries(entries_data):
            print("Entries are vaid")
            break

    return entries_data


def validate_entries(bottles):
    """
    Convert all string values into integers,
    Raises ValueError if strings cannot be
    converted into integers, if there aren't
    exactly 5 values, or if the values entered
    cannot be divided by 6.
    """
    try:
        [int(bottle) for bottle in bottles]
        if len(bottles) != 5:
            raise ValueError(
                f"The user must enter exactly 5 values,"
                f" you provided {len(bottles)}"
            )
    except ValueError as e:
        print(f"Invalid entries: {e}, please try again.\n")
        return False
    # - Checking if a string can be converted into an integer
    # - and use modulo operator to check if the integers can
    # - be devided by 6.
    for bottle in bottles:
        if bottle.isdigit():
            if int(bottle) % 6 != 0:
                print(f"{int(bottle)} is not divisible by 6.\n")
                return False
    return True


def update_entries_data(entries):
    """
    Update the entries worksheet with data
    prited from the user.
    """
    print("Entries worksheet updating...\n")
    # Assign the user input to the specific columns
    # of entries worksheet
    entries_worksheet = SHEET.worksheet("entries")
    entries_worksheet.append_row(entries)
    print("Entries worksheet updated successfully.\n")


def update_total_stock_data(total_stock):
    """
    Update the total_stock worksheet with the result
    obtained from adding the initial stock with the
    entries added by the user.
    """
    print("Total stock worksheet updating...\n")
    # Pass the values obtained after the addition
    # of intial_stock with entries to total_stock
    # worksheet rows
    total_stock_worksheet = SHEET.worksheet("total_stock")
    total_stock_worksheet.append_row(total_stock)
    print("Total stock worksheet updated successfully.\n")


def calculate_total_stock(entries_row):
    """
    Add entries to initial stock to get the final
    stock existing in the bar.
    -Initial stock represents the number of bottles
    per each drink that exist in the bar before entries.
    -Entries represents the number of bottles that were
    added to the initial stock to create a bigger stock
    for the current day's sale.
    """
    print("Calculating total stock...")
    # Import initial stock data from worksheet
    initial_stock = SHEET.worksheet("initial_stock").get_all_values()
    initial_stock_row = initial_stock[-1]

    total_stock_bottles = []
    for initial_stock, entries in zip(initial_stock_row, entries_row):
        total_stock = int(initial_stock) + entries
        total_stock_bottles.append(total_stock)

    return total_stock_bottles


def main():
    """
    Function create to hold
    and run all program funtions
    """
    entries = get_entries_data()
    entries_data = [int(entry) for entry in entries]
    update_entries_data(entries_data)
    final_total_stock = calculate_total_stock(entries_data)
    update_total_stock_data(final_total_stock)


print("Welcome to Garden Bar stock calculation!\n")
main()