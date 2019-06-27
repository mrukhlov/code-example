#-*- encoding:utf8 -*-

import pymorphy2
import itertools
from itertools import groupby
from operator import itemgetter
import xlwt, xlrd
from xlutils.copy import copy
import os


morph = pymorphy2.MorphAnalyzer()

template = [['top', 'acm__gent_plur', 'region__gent'], ['acm', 'region__gent', 't_cheaply' ], ['acm', 'region__loct', 'price'], ['t_look', 'acm', 't_in_center', 'region__gent', u'?']]

acm = [
	u'гостиница',
	u'хостел',
	u'гостевой дом',
	u'отель',
]

corpora = {
't_cheaply': [
	u'недорого',
	u'дешево',
],
'price': [
	u'цены',
	u'цена',
],
't_look': [
	u'Ищете цены на',
	u'Цены на',
	u'Ищете',
],
't_in_center': [
	u'в центре',
	u'центр',
],
'top': [
	u'Широкий выбор',
	u'Список',
	u'Выбор',
	u'Топ'
],
}

region_morphology = {
	'nomn': u'Москва',
	'gent': u'Москвы',
	'datv': u'Москве',
	'loct': u'в Москве',
}

acm_exceptions = [u'хостел', u'гостевой дом']

'''def case_generator(word):
	region_morphology.clear()
	#map(lambda i: region_morphology.update({i.tag.case: i[0]}) if len(i[0]) > 1 else None, morph.parse(word)[0].lexeme)
	#смотрим на число локейшна и берем падежи в том же числе (москва-набережные челны(санкт-петербург))
	#проверка по fixd потому что для москвы все параметры тега идентичные кроме его и abbr, а оно может понадобиться для ограничения по знакам (жалко только, что аббревиатуры не для всех морфем есть)
	#map(lambda i: region_morphology.update({i.tag.case: i[0]}) if 'Fixd' not in i.tag and i.tag.number == morph.parse(word)[0].tag.number else None, morph.parse(word)[0].lexeme)
	#map(lambda i: region_morphology.update({i.tag.case: i[0]}) if 'Abbr' not in i.tag and i.tag.number == morph.parse(word)[0].tag.number else None, morph.parse(word)[0].lexeme)
	map(lambda i: region_morphology.update({i.tag.case: i[0]}) if len(i[0]) > 1 and i.tag.number == morph.parse(word)[0].tag.number else None, morph.parse(word)[0].lexeme)
	#пиморфи не добавляет предлог для локатива
	region_morphology['loct'] = u'в ' + region_morphology['loct']'''

def case_generator(word):
	region_morphology_part = {}
	#map(lambda i: region_morphology.update({i.tag.case: i[0]}) if len(i[0]) > 1 else None, morph.parse(word)[0].lexeme)
	#смотрим на число локейшна и берем падежи в том же числе (москва-набережные челны(санкт-петербург))
	#проверка по fixd потому что для москвы все параметры тега идентичные кроме его и abbr, а оно может понадобиться для ограничения по знакам (жалко только, что аббревиатуры не для всех морфем есть)
	#map(lambda i: region_morphology.update({i.tag.case: i[0]}) if 'Fixd' not in i.tag and i.tag.number == morph.parse(word)[0].tag.number else None, morph.parse(word)[0].lexeme)
	#map(lambda i: region_morphology.update({i.tag.case: i[0]}) if 'Abbr' not in i.tag and i.tag.number == morph.parse(word)[0].tag.number else None, morph.parse(word)[0].lexeme)
	#map(lambda i: region_morphology.update({i.tag.case: i[0]}) if len(i[0]) > 1 and i.tag.number == morph.parse(word)[0].tag.number else None, morph.parse(word)[0].lexeme)
	map(lambda i: region_morphology_part.update({i.tag.case: i[0]}) if len(i[0]) > 1 and i.tag.number == morph.parse(word)[0].tag.number else None, morph.parse(word)[0].lexeme)
	#пиморфи не добавляет предлог для локатива
	if region_morphology_part.has_key('loct'):
		region_morphology_part['loct'] = u'в ' + region_morphology_part['loct']
	region_morphology[word] = region_morphology_part

def conc(word, case, temp_elem):
	exep = [u"ая", u"ий", u"яя", u"ие", u"ов", u"ач", u"ень", u"ые", u"ино", u"ое", u"ой", u"ый"]
	word_sep = word.replace('-', ' ').split(' ')
	case_1 = case
	#не рассматриваем анноуны
	if len(word_sep) == 2 and word_sep[0][-2:] in exep:
		if word_sep[0].endswith(u'т'):
			case = 'nomn'
		num = morph.parse(word_sep[0])[0].tag.number
		word_out = morph.parse(word_sep[0])[0].inflect({case, num})[0] + ' ' + morph.parse(word_sep[1])[0].inflect({case_1, num})[0]
		if case == 'loct':
			word_out = u'в ' + word_out
		return word_out
	else:
		if region_morphology[word].has_key(case):
			return region_morphology[word][temp_elem.split('__')[1]]
		else:
			return word

def acm_parameters_parse(elem):
	param = elem.split('__')[1].split('_')
	acm_case = param[0]
	acm_number = param[1]
	return acm_case, acm_number

#группировка в acm
def iter_dict_set(args_list, template_acm, template):
	iter_dict = {}
	template_iter = itertools.product(*args_list)
	template_iter_list = map(lambda x:list(x), template_iter)
	template_iter_list.sort(key=itemgetter(template.index(template_acm)))
	for elt, items in groupby(template_iter_list, itemgetter(template.index(template_acm))):
		iter_list = list(items)
		items_list = [item for item in iter_list]
		iter_dict.update({elt: items_list})
	return iter_dict

#фильтрация по размеру
def size_fit(iter_dict, limit):
	fit_dict = {}
	for i in iter_dict:
		#fit_dict.update({i: map(lambda x: ' '.join(x), iter_dict[i])[map(lambda x: len(x), map(lambda x: ' '.join(x), iter_dict[i])).index(max(filter(lambda x: x <= limit, map(lambda x: len(x), map(lambda x: ' '.join(x), iter_dict[i])))))]})
		strings = map(lambda x: ' '.join(x).replace(' ?', '?').replace('ё'.decode('utf8'), 'е'.decode('utf8')).capitalize(), iter_dict[i])
		lens_list = map(lambda x: len(x), strings)
		filtered = filter(lambda x: x <= limit, lens_list)
		if len(filtered) > 0:
			fit_dict.update({i: strings[lens_list.index(max(filtered))]})
		else:
			continue
	return fit_dict

def excel_write(fit_dict, city, path):
	if os.path.exists(path) == True:
		rb = xlrd.open_workbook(path, formatting_info=True, on_demand=True)
		sheet_rb = rb.sheet_by_index(0)
		col_0 = sheet_rb.col_values(0)

		book = copy(rb)
		sheet = book.get_sheet(0)
		dict_list = map(lambda x: fit_dict[x], fit_dict)
		for num in range(0, len(dict_list)):
			sheet.write(len(col_0) + num, 0, dict_list[num])
	else:
		book = xlwt.Workbook(encoding="utf-8")
		sheet = book.add_sheet(city, cell_overwrite_ok=True)
		dict_list = map(lambda x: fit_dict[x], fit_dict)
		for num in range(0, len(dict_list)):
			sheet.write(num, 0, dict_list[num])
	book.save('C:/test/ostrovok1.xls')

def txt_write(fit_dict, path):
	for y in fit_dict:
		with open(path, 'a') as f:
			f.write(fit_dict[y].encode('utf8') + '\n')

def text_generator(template, corpora, city, limit, path):
	with open(path, 'a') as f:
		f.write('\n' + ' '.join(template) + '\n\n')
	args_list = []
	#добавляю листы со значениями корпуса в args_list
	for temp_elem in template:
		#проверка на acm, т.к. acm не входит в словарь корпуса
		if temp_elem.find('acm') > -1:
			template_acm = temp_elem
			#проверка на грамматические параметры для acm
			if temp_elem.find('__') < 0:
				args_list.append(acm)
			else:
				acm_case, acm_number = acm_parameters_parse(temp_elem)
				#args_list.append([morph.parse(acm_elem.upper())[0].inflect({acm_case, acm_number})[0] for acm_elem in acm if acm_elem not in acm_exceptions])
				#приходится руками склонять гостевой дом и хостел
				acm_list = []
				for acm_elem in acm:
					if acm_elem == u'хостел':
						for morph_parse_elem in morph.parse(acm_elem):
							if 'NOUN' in morph_parse_elem.tag and morph_parse_elem.tag.gender == 'masc' and morph_parse_elem.tag.case == 'accs':
								acm_list.append(morph_parse_elem.inflect({acm_case, acm_number})[0])
					elif acm_elem == u'гостевой дом':
						guesthouse = morph.parse(u'гостевой')[5].inflect({acm_case, acm_number})[0] + ' ' + morph.parse(u'дом')[1].inflect({acm_case, acm_number})[0]
						acm_list.append(guesthouse)
					else:
						acm_list.append(morph.parse(acm_elem.upper())[0].inflect({acm_case, acm_number})[0])
				args_list.append(acm_list)
		else:
			#проверка на локейшн
			if temp_elem.find('region') > -1:
				if type(city) == list:
					for city_list_item in city:
						if region_morphology.has_key(city_list_item) == False:
							case_generator(city_list_item)
					city_list_cased = [conc(city_elem, temp_elem.split('__')[1], temp_elem) for city_elem in city]
					args_list.append(city_list_cased)
				else:
					if region_morphology.has_key(city) == False:
						case_generator(city)
					args_list.append([conc(city, temp_elem.split('__')[1], temp_elem)])

			else:
				#проверка на ключ словаря (для случаев со знаками препинания)
				if corpora.get(temp_elem) != None:
					args_list.append(corpora[temp_elem])
				else:
					args_list.append(list(temp_elem))
	#кидаем варианты стринги в лист
	iter_dict = iter_dict_set(args_list, template_acm, template)
	fit_dict = size_fit(iter_dict, limit)
	#excel_write(fit_dict, city, path)
	txt_write(fit_dict, path)

if __name__ == '__main__':
	path = 'C:/test/ostrovok.txt'
	with open(path, 'w') as f:
		f.write('')
	#text_generator(['acm', 'region__gent', 't_cheaply'], corpora, u'Сочи', 33, path)
	map(lambda temp: text_generator(temp, corpora, [u'санкт петербург', u'петербург', u'спб'], 33, path), template)
	map(lambda temp: text_generator(temp, corpora, u'москва', 33, path), template)
	map(lambda temp: text_generator(temp, corpora, u'сочи', 33, path), template)
	map(lambda temp: text_generator(temp, corpora, u'чебоксары', 33, path), template)
	map(lambda temp: text_generator(temp, corpora, [u'набережные челны', u'челны'], 33, path), template)