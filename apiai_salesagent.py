#-*- encoding:utf8 -*-

import xlrd
import sys
import shutil
import os
import sys
import fnmatch
import re
import gspread
import json
from oauth2client.client import SignedJwtAssertionCredentials
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

'''os.chdir('C:\\test\\')
json_key = json.load(open('salesagent-b127ac9b7577.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc = gspread.authorize(credentials)

#sh = gc.open("API:Localization")
sh = gc.open_by_key('')
prod_list = sh.worksheet("Product List")
sales = sh.worksheet("Sales")'''

json_key = {
  "type": "service_account",
  "project_id": "salesagent-146810",
  "client_id": "109934949107825453798",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
}

def gsheets_auth():
    #json_key = json.loads(key)
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key('')
    prod_list = sh.worksheet("Product List")
    sales = sh.worksheet("Sales")
    return sales

sales = gsheets_auth()

#print prod_list.acell('B2').value
#print sales.get_addr_int(sales.find('Nick').row, sales.find('Nick').col), sales.find('Nick').value

'''id_list = [i for i in sales.col_values(sales.find('Transaction ID').col)[1:] if len(i) > 0]
date_list = [i for i in sales.col_values(sales.find('Date').col)[1:] if len(i) > 0]
sales_rep_list = [i for i in sales.col_values(sales.find('Sales Rep').col)[1:] if len(i) > 0]
product = [i for i in sales.col_values(sales.find('Product').col)[1:] if len(i) > 0]
count_list = [i for i in sales.col_values(sales.find('Count').col)[1:] if len(i) > 0]
ppu_list = [int(float(i.replace('$', '').replace(',', ''))) for i in sales.col_values(sales.find('Price per unit').col)[1:] if len(i) > 0]
price_total_list = [int(float(i.replace('$', '').replace(',', ''))) for i in sales.col_values(sales.find('Price total').col)[1:] if len(i) > 0]
status_list = [i for i in sales.col_values(sales.find('Status').col)[1:] if len(i) > 0]'''

#status

'''$transaction_id status/Is $transaction_id paid?
status_dict = dict(zip(id_list, status_list))

print status_dict'''

#break

def parameters_extractor(params):
	dicts = [params]
	values = []

	while len(dicts):
		d = dicts.pop()

		for value in d.values():
			if isinstance(value, dict):
				dicts.append(value)
			elif isinstance(value, basestring) and len(value) > 0:
				values.append(value)

	return values

parameters = {
	#"date": "12/13/2015",
	"date": {"date-period":"2016-11-01/2016-11-30"},
	#"name": "Nick",
	#"product": "Hub",
	#"transaction-id": ""
}

parameters['date']['date-period'] = [datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%m/%d/%Y') for x in parameters['date']['date-period'].split('/')]
action = 'sales.product.best_selling'

sales_rep_sale_dict = {}

if len(parameters['date']) > 0:
	if parameters['date'].has_key('date'):
		for i in [i for i in sales.get_all_values() if len(i[1]) > 0 and i[1] == parameters['date']['date']]:
			num = int(float(i[4].replace('$', '').replace(',', '')))
			if sales_rep_sale_dict.has_key(i[3]) == False:
				sales_rep_sale_dict[i[3]] = num
			else:
				sales_rep_sale_dict[i[3]] += num
	else:
		for i in [i for i in sales.get_all_values()[1:] if
		          len(i[1]) > 0 and datetime.datetime.strptime(parameters['date']['date-period'][0],
		                                                       '%m/%d/%Y') <= datetime.datetime.strptime(i[1],
		                                                                                                 '%m/%d/%Y') <= datetime.datetime.strptime(
				          parameters['date']['date-period'][1], '%m/%d/%Y')]:
			num = int(float(i[4].replace('$', '').replace(',', '')))
			if sales_rep_sale_dict.has_key(i[3]) == False:
				sales_rep_sale_dict[i[3]] = num
			else:
				sales_rep_sale_dict[i[3]] += num
else:
	for i in [i for i in sales.get_all_values()[1:] if len(i[1]) > 0]:
		num = int(float(i[4].replace('$', '').replace(',', '')))
		if sales_rep_sale_dict.has_key(i[3]) == False:
			sales_rep_sale_dict[i[3]] = num
		else:
			sales_rep_sale_dict[i[3]] += num

# max_quantity = int(float(sales.cell(sales.find(max(sales_rep_sale_dict)).row, sales.find(max(sales_rep_sale_dict)).col+1).value.replace('$', '').replace(',', '')))
for i in sales_rep_sale_dict:
	if action == 'sales.product.best_selling':
		if sales_rep_sale_dict[i] == max(sales_rep_sale_dict.values()):
			max_sales_rep_sale = i
	elif action == 'sales.product.least_selling':
		if sales_rep_sale_dict[i] == min(sales_rep_sale_dict.values()):
			max_sales_rep_sale = i

print sales_rep_sale_dict
print sales.findall(str(sales_rep_sale_dict[max_sales_rep_sale]))
print sales.findall(max_sales_rep_sale)
print [i.value for i in sales.findall(max_sales_rep_sale)]

response = "We've sold " + str(sales_rep_sale_dict[max_sales_rep_sale]) + " units of " + str(
	max_sales_rep_sale) + " for the total of " + str(
	sales.cell(sales.find(max_sales_rep_sale).row, sales.find(max_sales_rep_sale).col + 3).value) + "."

print response

for i in sales.findall(max_sales_rep_sale):
	for ii in sales.findall(str(sales_rep_sale_dict[max_sales_rep_sale])):
		if i.row == ii.row:
			print i, ii



    
#parameters_list = filter(lambda x: x if len(x) > 0 else None, parameters.values())
#response_list = [x[7] for x in filter(lambda x: x if len(parameters_list) == len(set(x).intersection(set(parameters_list))) else None, sales.get_all_values())]
#parameters_list = filter(lambda x: x if len(x) > 0 else None, parameters.values())
'''parameters_list = parameters_extractor(parameters)
print parameters_list
#print [x[0] for x in filter(lambda x: x if len(parameters_list) == len(set(x).intersection(set(parameters_list))) else None, sales.get_all_values())]
print [x[2] for x in filter(lambda x: x if len(parameters_list) == len(set(x).intersection(set(parameters_list))) else None, sales.get_all_values())]
print filter(lambda x: x if len(parameters_list) == len(set(x).intersection(set(parameters_list))) else None, sales.get_all_values())'''
#parameters_list = ['Hub']
#time_period_matched_list = filter(lambda x: x if datetime.datetime.strptime("10/01/2016", '%m/%d/%Y') <= datetime.datetime.strptime(x[1], '%m/%d/%Y') <= datetime.datetime.strptime("10/29/2016", '%m/%d/%Y') else None, sales.get_all_values()[1:])

#response_num = reduce(lambda x, y: x + y, [int(float(i[6].replace('$', '').replace(',', ''))) for i in time_period_matched_list if len(parameters_list) == len(set(i).intersection(set(parameters_list)))])
#print response_num
'''asd = {}
date_filterd_list = filter(lambda x: x if x[1] == '12/13/2015' else None, sales.get_all_values())
for i in date_filterd_list:
	if i[3] not in asd:
		asd[i[3]] = [i[4],i[6]]
print {i[3]: [i[4],i[6]] for i in date_filterd_list}'''

#print filter(lambda x: x if len(x[1]) >0 and datetime.datetime.strptime("10/01/2016", '%m/%d/%Y') <= datetime.datetime.strptime(x[1], '%m/%d/%Y') <= datetime.datetime.strptime("10/29/2016", '%m/%d/%Y') else None, sales.get_all_values()[1:])



