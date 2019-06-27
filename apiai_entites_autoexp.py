import shutil
import os
import sys
import fnmatch
import re
import zipfile
import json
import urllib
import requests
import xlrd

from _apiai_methods import *


def chdir(path):
	try:
		os.chdir(path)
	except(WindowsError):
		os.makedirs(path)

path = 'C:/test/domains/entities'


'''rb = xlrd.open_workbook('C:/test/intents.xlsx', on_demand=True)
sheet_rb = rb.sheet_by_index(2)
col_0 = sheet_rb.col_values(0)
col_1 = sheet_rb.col_values(1)
xlsx_dict = dict(zip(col_0, col_1))'''

def autoexp():

	for root, dirnames, filenames in os.walk(path):
		for file in filenames:
			json_file_path = root + '/' + file
			with open(json_file_path, 'r') as f:
				json_file = json.loads(f.read())
				autoexp = json_file['automatedExpansion']
				if autoexp == True:
					zh_entity_path = json_file_path.replace('domains', 'domains_zh')
					#print 'true ', zh_entity_path
					try:
						with open(zh_entity_path, 'r+') as ff:
							domains_json_file = json.loads(ff.read())
							domains_json_file['automatedExpansion'] = True
							if domains_json_file['automatedExpansion'] != True:
								print 'wrong autoexp parameter (must be true) ', zh_entity_path
					except IOError:
						print 'error true', zh_entity_path
				else:
					zh_entity_path = json_file_path.replace('domains', 'domains_zh')
					#print 'false ', zh_entity_path
					try:
						with open(zh_entity_path, 'r+') as ff:
							domains_json_file = json.loads(ff.read())
							domains_json_file['automatedExpansion'] = False
							if domains_json_file['automatedExpansion'] != False:
								print 'wrong autoexp parameter (must be false) ', zh_entity_path
					except IOError:
						print 'error false', zh_entity_path

autoexp()


def autoexp_check():
	dict = {"app-store-name.json":"FALSE","astronomical-object.json":"FALSE","car-topic.json":"FALSE","continent.json":"FALSE","currency.json":"FALSE","device-module.json":"FALSE","disease.json":"FALSE","drug-name.json":"FALSE","event-type.json":"FALSE","fitness-app.json":"FALSE","food-product.json":"TRUE","food-tracking-service.json":"FALSE","geo-object-type.json":"FALSE","homework-subject.json":"FALSE","index-name.json":"FALSE","island.json":"FALSE","jokes-service.json":"FALSE","language.json":"FALSE","map-shortcut.json":"FALSE","meal.json":"FALSE","media.json":"FALSE","medicine-name.json":"FALSE","messages-service.json":"FALSE","movie-director.json":"FALSE","movie-genre.json":"FALSE","movie-service.json":"FALSE","movie.json":"TRUE","music-album.json":"TRUE","music-artist.json":"TRUE","music-genre.json":"FALSE","music-service.json":"FALSE","navigation-service.json":"FALSE","new-york-areas.json":"FALSE","occasion.json":"FALSE","outdoor-activity.json":"FALSE","outfit.json":"FALSE","painter.json":"FALSE","painting.json":"FALSE","paris-areas.json":"FALSE","paris-metro-stations.json":"FALSE","playlist.json":"FALSE","politician.json":"FALSE","prefecture.json":"FALSE","product.json":"FALSE","province.json":"FALSE","radio-program.json":"TRUE","radio-station.json":"FALSE","river.json":"FALSE","sculpture.json":"FALSE","search-engine.json":"FALSE","site.json":"FALSE","song.json":"TRUE","sort-param.json":"FALSE","sport-team.json":"FALSE","sportsman.json":"FALSE","station.json":"TRUE","translation-service.json":"FALSE","tv-channel.json":"FALSE","tv-show.json":"FALSE","unit-speed.json":"FALSE","user-contact.json":"TRUE","user-shortcut.json":"TRUE","venue-accomodation-chain.json":"TRUE","venue-accomodation-title.json":"TRUE","venue-arts-entertainment-title.json":"TRUE","venue-arts-entertainment-type.json":"FALSE","venue-automotive-chain.json":"TRUE","venue-automotive-title.json":"TRUE","venue-beauty-chain.json":"TRUE","venue-beauty-title.json":"TRUE","venue-beauty-type.json":"FALSE","venue-eating-out-chain.json":"TRUE","venue-eating-out-title.json":"TRUE","venue-eating-out-type.json":"FALSE","venue-education-title.json":"TRUE","venue-education-type.json":"FALSE","venue-facility.json":"TRUE","venue-local-service-title.json":"TRUE","venue-local-service-type.json":"FALSE","venue-medical-chain.json":"TRUE","venue-medical-title.json":"TRUE","venue-medical-type.json":"FALSE","venue-nightlife-chain.json":"TRUE","venue-nightlife-title.json":"TRUE","venue-nightlife-type.json":"FALSE","venue-outdoor-title.json":"TRUE","venue-outdoor-type.json":"FALSE","venue-shopping-chain.json":"TRUE","venue-shopping-title.json":"TRUE","venue-shopping-type.json":"FALSE","venue-sport-chain.json":"TRUE","venue-sport-title.json":"TRUE","venue-sport-type.json":"FALSE","venue-tourist-attraction-title.json":"TRUE","venue-travel-chain.json":"TRUE","venue-travel-title.json":"TRUE","venue-travel-type.json":"FALSE","video-service.json":"TRUE","war-title.json":"FALSE","actor.json":"FALSE","address.json":"FALSE","agent-name.json":"FALSE","air-direction.json":"FALSE","airline.json":"FALSE","airport.json":"FALSE","all.json":"FALSE","animal.json":"FALSE","app-name.json":"FALSE","artwork.json":"FALSE","automode.json":"FALSE","beverage-hard-drinks.json":"FALSE","beverage-soft-drinks.json":"FALSE","beverage.json":"FALSE","board-type.json":"FALSE","book-format.json":"FALSE","book.json":"FALSE","browser.json":"FALSE","building.json":"FALSE","call-type.json":"FALSE","car-device.json":"FALSE","car-door.json":"FALSE","car-light.json":"FALSE","car-mirror.json":"FALSE","car-part.json":"FALSE","car-seat.json":"FALSE","car-window.json":"FALSE","change-by.json":"FALSE","change-to.json":"FALSE","change-value.json":"FALSE","class.json":"FALSE","color.json":"FALSE","company-name.json":"FALSE","composer.json":"FALSE","condition.json":"FALSE","constant.json":"FALSE","contact.json":"FALSE","country.json":"FALSE","cuisine.json":"FALSE","date-time.json":"FALSE","dayofweek.json":"FALSE","delivery-product.json":"FALSE","device-action.json":"FALSE","device-volume.json":"FALSE","device.json":"FALSE","dialect.json":"FALSE","dish.json":"FALSE","domain.json":"FALSE","email-type.json":"FALSE","family-member.json":"FALSE","final-value.json":"FALSE","flight-address.json":"FALSE","food.json":"FALSE","game.json":"FALSE","geo-city.json":"FALSE","geo-object-title.json":"FALSE","given-name.json":"FALSE","heating.json":"FALSE","holiday.json":"FALSE","images-service.json":"FALSE","last-name.json":"FALSE","lights.json":"FALSE","lock.json":"FALSE","london-areas.json":"FALSE","map-sort.json":"FALSE","mountain.json":"FALSE","movie-tvshow.json":"FALSE","music-sort.json":"FALSE","music.json":"FALSE","musician.json":"FALSE","name-type.json":"FALSE","nationality.json":"FALSE","navigation-address.json":"FALSE","navigation-road-type.json":"FALSE","navigation-route-type.json":"FALSE","news-sort.json":"FALSE","news-source.json":"FALSE","nonstop.json":"FALSE","nutrient.json":"FALSE","open.json":"FALSE","person.json":"FALSE","phone-type.json":"FALSE","planet.json":"FALSE","populated-place.json":"FALSE","position.json":"FALSE","public-transport-type.json":"FALSE","rating.json":"FALSE","recurrence.json":"FALSE","refundable.json":"FALSE","room-facility.json":"FALSE","room.json":"FALSE","route.json":"FALSE","sea.json":"FALSE","service-name.json":"FALSE","service.json":"FALSE","sort.json":"FALSE","speaker.json":"FALSE","state-us.json":"FALSE","summary.json":"FALSE","temperature.json":"FALSE","ticket-type.json":"FALSE","time-format.json":"FALSE","time-zone.json":"FALSE","topic.json":"FALSE","traffic-event.json":"FALSE","unit-area.json":"FALSE","unit-information.json":"FALSE","unit-length.json":"FALSE","unit-temperature.json":"FALSE","unit-time.json":"FALSE","unit-volume.json":"FALSE","unit-weight.json":"FALSE","unit.json":"FALSE","user-name.json":"FALSE","venue-accomodation-type.json":"FALSE","venue-automotive-type.json":"FALSE","venue-chain.json":"FALSE","venue-sport-type.json":"FALSE","venue-title.json":"FALSE","venue-type.json":"FALSE","video.json":"FALSE","weather-condition.json":"FALSE","writer.json":"FALSE","zodiac-sign.json":"FALSE","adm-division-br.json":"FALSE","adm-division-cn.json":"FALSE","adm-division-de.json":"FALSE","adm-division-es.json":"FALSE","adm-division-fr.json":"FALSE","adm-division-gb.json":"FALSE","adm-division-it.json":"FALSE","adm-division-jp.json":"FALSE","adm-division-kr.json":"FALSE","adm-division-ru.json":"FALSE","adm-division-ua.json":"FALSE","adm-division-us.json":"FALSE","adm-division-za.json":"FALSE"}

	print dict["app-store-name.json"]

	for root, dirnames, filenames in os.walk(path):
		for file in filenames:
			json_file_path = root + '/' + file
			with open(json_file_path, 'r') as f:
				json_file = json.loads(f.read())
				autoexp = json_file['automatedExpansion']
				try:
					if str(autoexp).upper() != dict[file]:
						print str(autoexp).upper(), file, dict[file]
				except KeyError:
					print 'error ', json_file_path

#autoexp_check()

def req_par():
	path = 'C:/test/domains/intents_es'
	for root, dirnames, filenames in os.walk(path):
		for file in filenames:
			json_file_path = root + '/' + file
			with open(json_file_path, 'r') as f:
				json_file = json.loads(f.read())
				autoexp = json_file['responses'][0]["parameters"]
				for i in autoexp:
					if 'required' in i:
						if i['required'] == True:
							print file