import shutil
import os
import sys
import fnmatch
import re
import zipfile
import json
import urllib
import requests
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import csv
import multiprocessing as mp
from functools import partial


def chdir(path):
	try:
		os.chdir(path)
	except(WindowsError):
		os.makedirs(path)

def work(xlsx_dict, ids, headers, i):
	res = None

	if terminating.is_set():
		return res

	try:
		if xlsx_dict.has_key(ids[i]):
			ids[i] = map(lambda x: re.sub('\s\(.*','',x.replace('\r', '')), xlsx_dict[ids[i]].split('\n'))
			if type(ids[i]) == list:
				rr = requests.get('http://openapi-stage/api/intents/' + i + '?v=20150910', headers=headers)
				parameters = json.loads(rr.text)['responses'][0]['parameters']
				intent_name = json.loads(rr.text)['name']
				intent_params = [ii['name'] for ii in parameters]
				if len(ids[i][0]) > 0 and ids[i][0] != '-':
					if len(ids[i]) != len(intent_params):
						if len(intent_params) > len(ids[i]):
							return [intent_name, i, list(set(intent_params) - set(ids[i])), '']
						else:
							return [str(intent_name), str(i), '', list(set(ids[i]) - set(intent_params))]
				else:
					if len(intent_params) > 0 and intent_params != '-':
						if len(ids[i]) != intent_params:
							if len(intent_params) > len(ids[i]):
								return [intent_name, i, list(set(intent_params) - set(ids[i])), '']
							else:
								return [str(intent_name), str(i), '', list(set(ids[i]) - set(intent_params))]
			else:
				pass
	except KeyboardInterrupt:
		terminating.set()
	except Exception as e:
		res = str(e)
		print res

	#return res


def initializer(_terminating):
	global terminating

	terminating = _terminating

def main():
	print 'im main'
	terminating = mp.Event()


	PROCESSESS_COUNT = 20

	pool = mp.Pool(
		processes=PROCESSESS_COUNT,
		initializer=initializer,
		initargs=(terminating,)
	)

	try:
		func = partial(work, xlsx_dict, ids, headers)
		data = pool.map(func, ids)
		return filter(lambda x: x if x != None else None, data)

	except KeyboardInterrupt:
		pool.terminate()
		pool.join()
		raise


if __name__ == '__main__':
	json_key = {}


	agents = {}


	def gsheets_classifier_auth():
		scope = ['https://spreadsheets.google.com/feeds']
		credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
		gc = gspread.authorize(credentials)
		sh = gc.open_by_key('')
		smalltalk = sh.worksheet("SmallTalk")
		ready = sh.worksheet("Ready")
		smarthome = sh.worksheet("SmartHome")
		wisdom = sh.worksheet("Wisdom")
		return smalltalk, ready, smarthome, wisdom


	def gsheets_parameters_stat_auth(name, num):
		scope = ['https://spreadsheets.google.com/feeds']
		credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
		gc = gspread.authorize(credentials)
		sh = gc.open_by_key('')
		sheets_list = [i.title for i in sh.worksheets()]
		if num > 0:
			if name not in sheets_list:
				sh.add_worksheet(name, 1000, 30)
			else:
				sh.del_worksheet(sh.worksheets()[[i.title for i in sh.worksheets()].index(name)])
				sh.add_worksheet(name, 1000, 30)

			worksheet = sh.worksheet(name)
			return worksheet
		else:
			if name in sheets_list:
				sh.del_worksheet(sh.worksheets()[[i.title for i in sh.worksheets()].index(name)])

	def dict_maker(sheet):
		action = sheet.col_values(sheet.find('Action').col)[1:]
		try:
			parameter = sheet.col_values(sheet.find('Parameters name').col)[1:]
		except:
			parameter = sheet.col_values(sheet.find('Parameters').col)[1:]
		ready_dict = dict(zip(action, parameter))
		return ready_dict

	print 'authenticating'

	smalltalk, ready, smarthome, wisdom = gsheets_classifier_auth()

	print 'create dict 1'
	smalltalk_dict = dict_maker(smalltalk)
	print 'create dict 2'
	ready_dict = dict_maker(ready)
	print 'create dict 3'
	smarthome_dict = dict_maker(smarthome)
	print 'create dict 4'
	wisdom_dict = dict_maker(wisdom)

	xlsx_dict = dict(smalltalk_dict)
	xlsx_dict.update(ready_dict)
	xlsx_dict.update(smarthome_dict)
	xlsx_dict.update(wisdom_dict)

	for i in agents:
		print i

		name = i
		token = agents[i][0]

		print 'taking intents data'
		headers = {'Authorization': 'Bearer ' + token,'Content-Type': 'application/json; charset=utf-8'}
		r = requests.get('', headers=headers)
		ids = {x['id']:x['name'] for x in json.loads(r.text)}
		#map(lambda x: ids.update({x['id']:x['name']}), json.loads(r.text))

		intents_list = main()

		if len(intents_list) > 0:

			domains = gsheets_parameters_stat_auth(i, len(intents_list))

			domains.update_cell(1,1,'Name')
			domains.update_cell(1,2,'Id')
			domains.update_cell(1,3,'To remove')
			domains.update_cell(1,4,'To add')

			x = 2
			for stroke in intents_list :

				cell_list_key_a = domains.range('A'+str(x)+':'+ str('D' + str(x)))

				y=0

				for cell in cell_list_key_a:
					cell.value = stroke[y]
					y+=1

					domains.update_cells(cell_list_key_a)
				x+=1

			data = {"text": agents[i][1] + ' Please check ' + name + ' agent intent parameters: <https://docs.google.com/spreadsheets/d/', 'username': 'lingsite_bot', 'channel': 'domains-v2', "mrkdwn": True}
			hook = 'https://hooks.slack.com/services/'
			r = requests.post(hook, data=json.dumps(data))
		else:
			domains = gsheets_parameters_stat_auth(i, len(intents_list))