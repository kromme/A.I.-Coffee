import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('drive_client_secret.json', scope)

gsheet = gspread.authorize(credentials)
gsheet = gsheet.open("virtual-assistant-coffee-link").sheet1


def get_willy_database_for_coffee():
	# get data
	data = gsheet.get_all_values()
	df = pd.DataFrame(data[1:], columns = data[0])

	return df


def check_coffee_added_to_willy_database():
	"""
	returns first ID of to brewing ID 
	"""
	df = get_willy_database_for_coffee()

	# check for new
	df = df[df.finished.astype(str) != "1"]

	# if no new, return False
	if len(df) == 0:
		return False

	return df.head(1).id.values[0]

def add_coffee_to_willy_database(drink):
	df = get_willy_database_for_coffee()
	index = len(df) + 2
	ids = [int(id.replace('id', '')) for id in df.id.values]
	newid = 'id{}'.format(max(ids) + 1)
	row = [newid, datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), drink, '0']
	gsheet.insert_row(row, index)


def update_coffee_from_willy_database(id):
	# find cell
	cell_list = gsheet.findall(id)
	
	# get cell row
	row = cell_list[0].row

	# update the finished column in the row with a 1
	gsheet.update_cell(row, 4, 1)



def brew_coffee(id):
	# 
	df = get_willy_database_for_coffee()

	# determine drink
	drink = df[(df.finished.astype(str) == "0") & (df.id.astype(str) == str(id))].coffee.values[0]
	drink = drink.lower()

	if not drink in ['coffee', 'espresso', 'hotchoc', 'cappuccino', 'hotwater']:
		print('{} not found, order something else'.format(drink))
		return False

	# brew the drink
	result = brew(ser, drink)
	print (result)
	print ('')

	# update database
	update_coffee_from_willy_database(id)
	return result

