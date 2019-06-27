# -*- coding: cp1251 -*-

import wikipedia
from bs4 import BeautifulSoup
import urllib2
import re
import os
import codecs
import sys
from urllib2 import HTTPError
    
def chdir(path):
    try:
        os.chdir(path)
    except(WindowsError):
        os.makedirs(path) 
        os.chdir(path)

#cat_list = ['Lists']
cat_list = []
#wiki_page = "http://en.wikipedia.org/wiki/List_of_lists_of_lists"
wiki_page = "https://en.wikipedia.org/wiki/List_of_NHL_players"
path = 'C://test//wiki_junk/'
page = urllib2.urlopen(wiki_page)
soup = BeautifulSoup(page)
try:
#else we got simple list page
    references = '<span class="mw-headline" id="References">References</span>'
    sources = '<span class="mw-headline" id="Sources">Sources</span>'
    see_also = '<span class="mw-headline" id="See_also">See also</span>'
    notes = '<span class="mw-headline" id="Notes">Notes</span>'
    footnotes = '<span class="mw-headline" id="Footnotes">Footnotes</span>'
    external_links = '<span class="mw-headline" id="External_links">External links</span>'
    for headline in soup('span', {'class' : 'mw-headline'}):
        if str(headline) != references and str(headline) != sources and str(headline) != see_also and str(headline) != notes and str(headline) != footnotes and str(headline) != external_links:
            links = headline.find_next('ul').find_all('a')
            for link in links:
                if link.text not in cat_list:
                    match = re.match('[Ll]ist(s*).*', link.text)
                    match_num = re.match('\[\d+\]', link.text)
                    match_alphabet = re.match('^[a-zA-Z0-9]{1}$', link.text)
                    if match:
                        http_match = re.search('http:', link['href'])
                        if not http_match:
                            list_link_text = 'https://en.wikipedia.org' + link['href']
                        elif http_match:
                            list_link_text = 'http://en.wikipedia.org' + link['href']
                        redlink_match = re.search('redlink', list_link_text)
                        match_symbols = re.search('[#:]', link['href'])
                        if not redlink_match and not match_symbols:
                            cat_list.append(list_link_text)
                            #uncomment to check added subcat
                            #print 'list added to cat_list: ' + list_link_text
                    #else:
        if str(headline) != references and str(headline) != sources and str(headline) != see_also and str(headline) != notes and str(headline) != footnotes and str(headline) != external_links:
            #links = headline.find_next('ul').find_all('a')
            links = headline.find_next('ul').find_all('li')
            for link in links:
                linkss = link.find_all('a')
                if linkss:
                    if linkss[0].text not in cat_list:
                        match = re.match('[Ll]ist(s*).*', linkss[0].text)
                        list_in_link = re.search('[Ll]ist(s*).*', linkss[0]['href'])
                        redlink_list_in_link = re.search('redlink', linkss[0]['href'])
                        match_num = re.match('\[\d+\]', linkss[0].text)
                        match_alphabet = re.match('^[a-zA-Z0-9]{1}$', linkss[0].text)
                        http_match = re.search('http:', linkss[0]['href'])
                        redlink_match = re.search('redlink', linkss[0]['href'])
                        match_symbols = re.search('[#:]', linkss[0]['href'])
                        if list_in_link and not redlink_list_in_link:
                            if http_match:
                                list_link_textt = 'http://en.wikipedia.org' + linkss[0]['href']
                            elif not http_match:
                                list_link_textt = 'https://en.wikipedia.org' + linkss[0]['href']
                            if list_link_textt not in cat_list:
                                if not match_symbols and not redlink_match:
                                    cat_list.append(list_link_textt)
                                    #print 'list added to cat_list: ' + list_link_textt
    #print 'overall lists quantity ' + str(len(links))
        #print 'added ' + link.text
except AttributeError:
    print subcat_page + " is wrong list page"

cat_list = ['Hotel_chains']

for elem in cat_list:
    #wiki_page = "https://de.wikipedia.org/wiki/Kategorie:%s" % elem
    wiki_page = "http://en.wikipedia.org/wiki/Category:%s" % elem
    #wiki_page = 'https://en.wikipedia.org/wiki/' + elem
    #wiki_page = 'https://en.wikipedia.org/wiki/List_of_NHL_players'
    #path = 'E://wiki_junk//wikitest-' + str(i) + '.txt'
    path = 'C://test/wiki_junk/'
    page = urllib2.urlopen(wiki_page)
    soup = BeautifulSoup(page)
    subcat = soup('div',{'class':'CategoryTreeItem'})
    pages_in_cat = soup('div',{'class':'mw-category-group'})

    #making list from subcat links
    subcat_list = []
    singer_list = []
    #for i in soup.select('.CategoryTreeItem'):
    if soup.select('div#mw-subcategories'):
        for i in soup.select('div#mw-subcategories'):
            for ii in i.find_all('a'):
                #link_text = 'https://de.wikipedia.org' + ii['href']
                link_text = 'https://en.wikipedia.org' + ii['href']
                if link_text not in subcat_list:
                    subcat_list.append(link_text)
                    subcat_name = str(ii['href'][15:])
    if soup.select('div#mw-pages'):
        for headline in soup.select('div#mw-pages'):
            #print i #print page
            links = headline.find_all('a')
            for link in links:
                link_replace = re.sub('\s\(.*\)', '', link.text)
                link_replace = re.sub('Template:', '', link_replace)
                link_match = re.match('learn more', link_replace)
                list_match = re.match('[Ll]ist(s*).*', link_replace)
                #processing pages list
                if not link_match and not list_match:
                    if link_replace not in singer_list:
                        singer_list.append(link_replace)
                if list_match:
                    #adding pages with list to main list
                    list_link_text = 'https://en.wikipedia.org' + link['href']
                    subcat_list.append(list_link_text)
    cat_path = path + str(elem)
    chdir(cat_path)
    
#singer_cat_filter = ['[C]har.*', '[Pp]eople[s]*', '[Cc]omedian[s]*', '[Ww]riter[s]*', '[Aa]ctor[s]*', '[Aa]ctress[es]*', '[Ii]dol[s]*', '[Cc]eleb.*', '[Ss]ong[s]*', '[Mm]en', '[Bb]ook[s]*', '[Ff]ilm[s]*', '[Ww]ork[s]*']
singer_cat_filter = []
singer_list = []
#subcat_list = []
used_subcat_list = []
#subcat_list.append('http://en.wikipedia.org/wiki/List_of_lists_of_lists')
#subcat_list.append('http://en.wikipedia.org/wiki/List_of_newspapers_in_Algeria')
#subcat_list.append('https://en.wikipedia.org/wiki/Lists_of_musicians')
#subcat_list.append('http://en.wikipedia.org/wiki/List_of_Lego_City_sets')

chdir(path + 'Lists')

del singer_list[:]
count = 0

del subcat_list[:]
del cat_list[:]
cat_list.append('https://zh.wikipedia.org/wiki/??????')
subcat_list.append('https://zh.wikipedia.org/wiki/??????')

for cat_page in cat_list:
    http = re.search('http:', str(cat_page))
    if http:
        cat_page_path = re.sub('_', ' ', str(cat_page[29:]))
    else:
        cat_page_path = re.sub('_', ' ', str(cat_page[30:]))
    cat_path = path + 'Lists/' + cat_page_path
    chdir(cat_path)
    subcat_list.append(cat_page)
    while len(subcat_list) > 0:
        for subcat_page in subcat_list:
            del singer_list[:]
            #testing section
            count += 1
            print 'now parsing: ' + subcat_page
            print 'subcat_list len = ' + str(len(subcat_list))
            #print 'initial singer_list len = ' + str(len(singer_list))
            print 'now parsing ' + str(count) + ' out of ' + str(len(subcat_list))
            #subcat_list.remove(subcat_page)
            #link_filter = re.search('people', subcat_page)
            #if not link_filter:
            chdir(cat_path)
            try:
                page = urllib2.urlopen(subcat_page)
            except NameError and HTTPError:
                pass
            soup = BeautifulSoup(page)
            next_page_link = soup.find('a', text='next page')
            lists_match = re.search('[Ll]ists', subcat_page)
            #lists_match = re.search('[Ll]ist(s*)', subcat_page)
            if next_page_link:
                link = 'https://en.wikipedia.org' + next_page_link['href']
                subcat_list.append(link)
            #check heading for 'list' word
            for headline in soup.select('h1#firstHeading'):
                match_List = re.match('[Ll]ist(s*).*', headline.text)
                match_Category = re.match('[Cc]ategory(s*).*', headline.text)
                if match_List:
                    #break
                    #check if there is a simple table on page
                    #https://en.wikipedia.org/wiki/List_of_Poles
                    if soup('table', {'class' : 'multicol'}):
                        print 1
                        for headline in soup('table', {'class' : 'multicol'}):
                            try:
                                links = headline.find_next('tr').find_all('td')
                                for link in links:
                                    linkk = link.find_next('ul').find_all('a')
                                    for linkkk in linkk:
                                        match = re.match('\[\d+\]', str(linkkk.text.encode('utf-8')))
                                        list_match = re.match('[Ll]ist(s*)', str(linkkk.text.encode('utf-8')))
                                        if not match and not list_match and not lists_match:
                                            if linkkk.text:
                                                singer_1st = re.sub(',', '', linkkk.text)
                                                singer_1st = re.sub('\(', '', linkkk.text)
                                                singer_1st = re.sub('\)', '', linkkk.text)
                                                singer_1st = re.sub('"', '', linkkk.text)
                                                singer_1st = re.sub('&', 'and', linkkk.text)
                                                singer_list.append(singer_1st)
                            except AttributeError:
                                pass
                    elif soup('div', {'class' : 'div-col columns column-width'}):
                        print 2
                        ref_div = 'div class="reflist references-column-width"'
                        for headline in soup('div', {'class' : 'div-col columns column-width'}):
                            if ref_div not in str(headline):
                                link = headline.find_all('a')
                                for linkk in link:
                                    match_List = re.search('[Ll]ist(s*).*', linkk.text)
                                    match_wiki = re.search('wiki', linkk['href'])
                                    if match_List:
                                        if match_wiki:
                                            link = 'https://en.wikipedia.org' + linkk['href']
                                            redlink_match = re.search('redlink', link)
                                            if not redlink_match:
                                                if link not in subcat_list and link not in used_subcat_list and link not in cat_list:
                                                    subcat_list.append(link)
                                                    print 'added ' + link
                                    else:
                                        num_match = re.match('\[\d+\]', linkk.text)
                                        cit_match = re.match('\[citation needed\]', linkk.text)
                                        if not num_match and not cit_match and not lists_match:
                                        #if not num_match and not cit_match:
                                            if linkk.text:
                                                singer_2nd = re.sub('\s\(.*\)', '', linkk.text)
                                                singer_2nd = re.sub(',', '', linkk.text)
                                                singer_2nd = re.sub('\(', '', linkk.text)
                                                singer_2nd = re.sub('\)', '', linkk.text)
                                                singer_2nd = re.sub('"', '', linkk.text)
                                                singer_2nd = re.sub('&', 'and', linkk.text)
                                                singer_list.append(singer_2nd)
                    #check if we got sortable table or multiple tables on list page
                    elif soup.find("table", { "class" : "wikitable sortable" }) or soup.find("table", { "class" : "wikitable" }):
                        print 3
                        if soup.find("table", { "class" : "wikitable sortable" }):
                            print 3.1
                            table = soup.find_all("table", { "class" : "wikitable sortable" })
                            for roww in table:
                                row_set = roww.findAll("tr")
                                for row in row_set:
                                    row_cells_set = row.findAll("td")
                                    if row_cells_set:
                                        if row_cells_set[0].text:
                                            match_num = re.match('\[\d+\]', row_cells_set[0].text)
                                            #match_num_col = re.match('[^a-zA-Z]+\d{1,3}', row_cells_set[0].text)
                                            match_num_col = re.match('^\d{1,3}$', row_cells_set[0].text)
                                            if not match_num:
                                                if not match_num_col:
                                                    item = row_cells_set[0].text
                                                else:
                                                    item = row_cells_set[1].text
                                                match_num_cell = re.match('\[\d+\]', item)
                                                if not match_num_cell and not lists_match:
                                                    singerr = re.sub(',', '', item)
                                                    singerr = re.sub('\s\(.*\)', '', singerr)
                                                    singerr = re.sub('\s*\[.*\]', '', singerr)
                                                    singerr = re.sub('-', '', singerr)
                                                    singerr = re.sub('—', '', singerr)
                                                    singerr = re.sub(',', '', singerr)
                                                    singerr = re.sub('\–', '', singerr)
                                                    singerr = re.sub(':', '', singerr)
                                                    singerr = re.sub('\'', ' ', singerr)
                                                    singerr = re.sub('\[\d+\]', '', singerr)
                                                    singerr = re.sub('\[.*\]', '', singerr)
                                                    singerr = re.sub('"', ' ', singerr)
                                                    split = singerr.split(" ")
                                                    if len(split) == 3:
                                                        try:
                                                            rep = split[1]
                                                            rep_len = len(split[1])
                                                            rep_index = rep_len
                                                            if rep[0:rep_index/2] == rep[rep_index/2:rep_index]:
                                                                if split[2]:
                                                                    singerr = rep[rep_index/2:rep_index] + ' ' + split[2]
                                                        except IndexError:
                                                            pass
                                                    elif len(split) == 5:
                                                        try:
                                                            middle = split[2]
                                                            sur = middle[0:len(split[3])]
                                                            name = middle[len(split[3]):]
                                                            if sur == split[3] and name == split[1]:
                                                                if split[2]:
                                                                    singerr = split[1] + ' ' + split[3] + ' ' + split[4]
                                                        except IndexError:
                                                            pass
                                                    elif len(split) == 7:
                                                        try:
                                                            middle = split[3]
                                                            sur = middle[0:len(split[5])]
                                                            name = middle[len(split[5]):]
                                                            if sur == split[5] and name == split[1]:
                                                                if split[3]:
                                                                    singerr = split[2] + ' ' + split[3] + ' ' + split[4] + ' ' + split[1]
                                                        except IndexError:
                                                            pass
                                                    #if singerr not in singer_list and not lists_match:
                                                    if singerr not in singer_list:
                                                        singer_list.append(singerr)
                        elif soup.find("table", { "class" : "wikitable" }):
                            print 3.2
                            table = soup.findAll("table", { "class" : "wikitable" })
                            for table in table:
                                row_set = table.findAll("tr")
                                for row in row_set:
                                    row_cells_set = row.findAll("td")
                                    if row_cells_set:
                                        match_num = re.match('\[\d+\]', row_cells_set[0].text)
                                        if not match_num:
                                            if row_cells_set[0].text and not lists_match:
                                            #if row_cells_set[0].text:
                                                link_replace = re.sub('\[\d+\]', '', row_cells_set[0].text)
                                                link_replace = re.sub('\s\(.*\)', '', link_replace)
                                                link_replace = re.sub(',', '', link_replace)
                                                link_replace = re.sub('\(', '', link_replace)
                                                link_replace = re.sub('\)', '', link_replace)
                                                link_replace = re.sub('"', '', link_replace)
                                                link_replace = re.sub('&', 'and', link_replace)
                                                link_replace = re.sub('\xa0', '', link_replace)
                                                #if link_replace not in singer_list:
                                                if link_replace.startswith(' '.decode('utf-8')):
                                                    singer_list.append(link_replace[1:])
                                                else:
                                                    singer_list.append(link_replace)
                        elif soup('table', {'class' : 'wikitable sortable plainrowheaders'}):
                            print 3.3
                            table = soup.find("table", { "class" : "wikitable sortable plainrowheaders" })
                            row_set = table.findAll("tr")
                            for row in row_set:
                                row_cells_set = row.findAll("td")
                                if row_cells_set:
                                    match_num = re.match('\[\d+\]', row_cells_set[0].text)
                                    if not match_num:
                                        if row_cells_set[0].text:
                                            sortkey_span = row_cells_set[0].findAll("span", { "class" : "sorttext" })
                                            for text in sortkey_span:
                                                singerr = re.sub('\s\(.*\)', '', text.text)
                                                singerr = re.sub('\s*\[.*\]', '', singerr)
                                                if singerr not in singer_list:
                                                    singer_list.append(singerr)
                    elif soup('div', {'class' : 'div-col columns column-count column-count-3'}):
                        print 6
                        for headline in soup('div', {'class' : 'div-col columns column-count column-count-3'}):
                            link = headline.find_next('ul').find_all('li')
                            for para_link in link:
                                if para_link:
                                    match_num = re.match('\[\d+\]', para_link.text)
                                    if not match_num:
                                        if para_link.text:
                                            link_replace = re.sub('\[\d+\]', '', para_link.text)
                                            link_replace = re.sub('\s\(.*\)', '', link_replace)
                                            link_replace = re.sub(',', '', link_replace)
                                            link_replace = re.sub('\(', '', link_replace)
                                            link_replace = re.sub('\)', '', link_replace)
                                            link_replace = re.sub('"', '', link_replace)
                                            link_replace = re.sub('&', 'and', link_replace)
                                            link_replace = re.sub('\xa0', '', link_replace)
                                            if link_replace not in singer_list:
                                                singer_list.append(link_replace)
                                            
                    else:
                        print 4
                        try:
                        #else we got simple list page
                            references = '<span class="mw-headline" id="References">References</span>'
                            sources = '<span class="mw-headline" id="Sources">Sources</span>'
                            see_also = '<span class="mw-headline" id="See_also">See also</span>'
                            notes = '<span class="mw-headline" id="Notes">Notes</span>'
                            footnotes = '<span class="mw-headline" id="Footnotes">Footnotes</span>'
                            external_links = '<span class="mw-headline" id="External_links">External links</span>'
                            notes_and_references = '<span class="mw-headline" id="Notes_and_references">Notes and references</span>'
                            para = soup.find('p').find_next('ul').find_all('a')
                            for para_link in para:
                                list_match = re.match('[Ll]ist(s*).*', para_link.text)
                                wiki_match = re.search('wiki', para_link['href'])
                                if wiki_match and list_match:
                                    list_link_text = 'https://en.wikipedia.org' + para_link['href']
                                    if list_link_text not in subcat_list and list_link_text not in used_subcat_list and list_link_text not in cat_list:
                                        redlink_match = re.search('redlink', list_link_text)
                                        dots_match = re.search('[#:]', para_link['href'])
                                        if not redlink_match and not dots_match:
                                            subcat_list.append(list_link_text)
                                            print 'list added to subcat_list: ' + list_link_text
                                else:
                                    singer_text = re.sub('\s\(.*\)', '', para_link.text)
                                    singer_text = re.sub(',', '', singer_text)
                                    singer_text = re.sub('\(', '', singer_text)
                                    singer_text = re.sub('\)', '', singer_text)
                                    singer_text = re.sub('"', '', singer_text)
                                    singer_text = re.sub('&', 'and', singer_text)
                                    if singer_text not in singer_list:
                                        singer_list.append(singer_text)
                            for headline in soup('span', {'class' : 'mw-headline'}):
                                if str(headline) != references and str(headline) != notes_and_references and str(headline) != sources and str(headline) != see_also and str(headline) != notes and str(headline) != footnotes and str(headline) != external_links:
                                    links = headline.find_next('ul').find_all('a')
                                    for link in links:
                                        if link.text not in singer_list:
                                            match = re.match('[Ll]ist(s*).*', link.text)
                                            match_num = re.match('\[\d+\]', link.text)
                                            match_alphabet = re.match('^[a-zA-Z0-9]{1}$', link.text)
                                            if match:
                                                http_match = re.search('http:', link['href'])
                                                wiki_match = re.search('wiki', link['href'])
                                                if wiki_match:
                                                    if not http_match:
                                                        list_link_text = 'https://en.wikipedia.org' + link['href']
                                                    elif http_match:
                                                        list_link_text = 'http://en.wikipedia.org' + link['href']
                                                    #if not link_filter_people or not link_filter_actor or not link_filter_work or not link_filter_film or not link_filter_book or not link_filter_men or not link_filter_comedian or not link_filter_writer or not link_filter_actor or not link_filter_actress or not link_filter_idols or not link_filter_celebs or not link_filter_songs:
                                                    res = False
                                                    for filter_iter in singer_cat_filter:   #part of iter filtering
                                                        filter_proc = re.search(filter_iter, link.text)
                                                        if not filter_proc:
                                                            if list_link_text not in subcat_list:
                                                                res = True
                                                        else:
                                                            res = False
                                                            break
                                                    if res:
                                                        if list_link_text not in subcat_list and list_link_text not in used_subcat_list and list_link_text not in cat_list:
                                                            redlink_match = re.search('redlink', list_link_text)
                                                            dots_match = re.search('[#:]', link['href'])
                                                            if not redlink_match and not dots_match:
                                                                subcat_list.append(list_link_text)
                                                                #uncomment to check added subcat
                                                                print 'list added to subcat_list: ' + list_link_text
                                            #else:
                                if str(headline) != references and str(headline) != notes_and_references and str(headline) != sources and str(headline) != notes and str(headline) != footnotes and str(headline) != external_links:
                                    #links = headline.find_next('ul').find_all('a')
                                    links = headline.find_next('ul').find_all('li')
                                    for link in links:
                                        linkss = link.find_all('a')
                                        if linkss:
                                            try:
                                                if linkss[0].text not in singer_list:
                                                    match = re.match('[Ll]ist(s*).*', linkss[0].text)
                                                    list_in_link = re.search('[Ll]ist(s*).*', linkss[0]['href'])
                                                    redlink_list_in_link = re.search('redlink', linkss[0]['href'])
                                                    match_num = re.match('\[\d+\]', linkss[0].text)
                                                    match_alphabet = re.match('^[a-zA-Z0-9]{1}$', linkss[0].text)
                                                    http_match = re.search('http:', linkss[0]['href'])
                                                    wiki_in_link = re.match('http[s*]://en.wikipedia', linkss[0]['href'])
                                                    if not match_num and not match_alphabet and not match and not list_in_link:
                                                        if link.text not in singer_list and not lists_match:
                                                        #if link.text not in singer_list:
                                                            singer_text = re.sub('\s\(.*\)', '', linkss[0].text)
                                                            singer_text = re.sub(',', '', singer_text)
                                                            singer_text = re.sub('\(', '', singer_text)
                                                            singer_text = re.sub('\)', '', singer_text)
                                                            singer_text = re.sub('"', '', singer_text)
                                                            singer_text = re.sub('&', 'and', singer_text)
                                                            if singer_text not in singer_list:
                                                                singer_list.append(singer_text)
                                                            #uncomment to check added singers
                                                            #print 'singer from list_page ' + singer_text
                                                            wiki_match = re.search('wiki', linkss[0]['href'])
                                                    if list_in_link and match and not redlink_list_in_link:
                                                        if wiki_match:
                                                            if http_match:
                                                                list_link_textt = 'http://en.wikipedia.org' + linkss[0]['href']
                                                            elif not http_match:
                                                                list_link_textt = 'https://en.wikipedia.org' + linkss[0]['href']
                                                            #list_link_textt = 'https://en.wikipedia.org' + linkss[0]['href']
                                                            if list_link_textt not in subcat_list and list_link_textt not in used_subcat_list and list_link_textt not in cat_list:
                                                                redlink_match = re.search('redlink', list_link_textt)
                                                                dots_match = re.search('[#:]', linkss[0]['href'])
                                                                if not redlink_match and not dots_match:
                                                                    subcat_list.append(list_link_textt)
                                                                    print 'list added to subcat_list1: ' + list_link_textt
                                                                    #print 'list added to subcat_list1: ' + linkss[0]['href']
                                            except KeyError:
                                                pass
                            print 'overall lists quantity ' + str(len(links))
                                #print 'added ' + link.text
                        except AttributeError:
                            print subcat_page + " is wrong list page"
                else:
                    print 5
                    if match_Category:
                        if soup.select('div#mw-pages'):
                            for headline in soup.select('div#mw-pages'):
                                #print subcat_page #print page
                                links = headline.find_all('a')
                                for link in links:
                                    link_replace = re.sub('\s\(.*\)', '', link.text)
                                    link_replace = re.sub('Template:', '', link_replace)
                                    link_replace = re.sub(',', '', link_replace)
                                    link_replace = re.sub('\(', '', link_replace)
                                    link_replace = re.sub('\)', '', link_replace)
                                    link_replace = re.sub('"', '', link_replace)
                                    link_replace = re.sub('&', 'and', link_replace)
                                    link_match = re.match('learn more', link_replace)
                                    list_match = re.match('[Ll]ist(s*).*', link_replace)
                                    next_match = re.match('next page', link_replace)
                                    wiki_match = re.search('wiki', link['href'])
                                    #processing pages list
                                    if not link_match and not list_match and not next_match and not lists_match:
                                    #if not link_match and not list_match and not next_match:
                                        #if link_replace not in singer_list:
                                        singer_list.append(link_replace)
                                        #print link_replace
                                            #print 'page from subcat_page ' + link_replace
                                            #with open(path, 'a')as f:
                                                #f.write(str(link_replace.encode('utf-8')) + '\n')
                                    if list_match:
                                        if wiki_match:
                                            #adding pages with list to main list
                                            list_link_text = 'https://en.wikipedia.org' + link['href']
                                            if list_link_text not in subcat_list and list_link_text not in used_subcat_list and list_link_text not in cat_list:
                                                redlink_match = re.search('redlink', list_link_text)
                                                if not redlink_match:
                                                    subcat_list.append(list_link_text)
                                                    print 'list found in pages in category: ' + list_link_text
                                print 'overall pages quantity ' + str(len(links))
                        if soup.select('div#mw-subcategories'):
                            for headline in soup.select('div#mw-subcategories'):
                                links = headline.find_all('a')
                                for link in links:
                                    wiki_match = re.search('wiki', link['href'])
                                    if wiki_match:
                                        #print 'added ' + link.text
                                        link_text = 'https://en.wikipedia.org' + link['href']
                                        #adding pages with subcategories to main list
                                        res = False
                                        for filter_iter in singer_cat_filter:
                                            filter_proc = re.search(filter_iter, link['href'])
                                            if not filter_proc:
                                                if link_text not in subcat_list:
                                                    res = True
                                            else:
                                                res = False
                                                break
                                        if res:
                                            if link_text not in subcat_list and link_text not in used_subcat_list and link_text not in cat_list:
                                                redlink_match = re.search('redlink', link_text)
                                                if not redlink_match:
                                                    subcat_list.append(link_text)
                                                    print 'category added: ' + link_text
                    else:
                        if soup.select('span.mw-headline'):
                            for headline in soup.select('p'):
                                try:
                                    links = headline.find_next('ul').find_all('li')
                                    for link in links:
                                        linkss = link.find_all('i')
                                        for i in linkss:
                                            link_replace = re.sub('\s\(.*\)', '', i.text)
                                            link_replace = re.sub('Template:', '', link_replace)
                                            link_replace = re.sub(',', '', link_replace)
                                            link_replace = re.sub('\(', '', link_replace)
                                            link_replace = re.sub('\)', '', link_replace)
                                            link_replace = re.sub('"', '', link_replace)
                                            link_replace = re.sub('&', 'and', link_replace)
                                            link_match = re.match('learn more', link_replace)
                                            list_match = re.match('[Ll]ist(s*).*', link_replace)
                                            next_match = re.match('next page', link_replace)
                                            try:
                                                wiki_match = re.search('wiki', i['href'])
                                            except KeyError:
                                                pass
                                            #processing pages list
                                            if not link_match and not list_match and not next_match and not lists_match:
                                            #if not link_match and not list_match and not next_match:
                                                if link_replace not in singer_list:
                                                    singer_list.append(link_replace)
                                            if list_match:
                                                if wiki_match:
                                                    #adding pages with list to main list
                                                    try:
                                                        list_link_text = 'https://en.wikipedia.org' + link['href']
                                                    except KeyError:
                                                        pass
                                                    if list_link_text not in subcat_list and list_link_text not in used_subcat_list and list_link_text not in cat_list:
                                                        redlink_match = re.search('redlink', list_link_text)
                                                        if not redlink_match:
                                                            subcat_list.append(list_link_text)
                                                        print 'list found in pages in category: ' + list_link_text
                                except AttributeError:
                                    pass
                                    
            file_name_re = re.search('[Cc]ategory:', str(subcat_page))
            http = re.search('http:', str(subcat_page))
            if file_name_re:
                if http:
                    file_name = subcat_page[38:]
                else:
                    file_name = subcat_page[39:]
                #chdir(file_name)
            else:
                if http:
                    file_name = subcat_page[29:]
                else:
                    file_name = subcat_page[30:]

            if singer_list:
                file_open_name = file_name + '.txt'
                slash_match = re.search('/', file_open_name)
                slash_meta_match = re.search('/', file_name)
                if slash_meta_match:
                    file_name = re.sub('/', '_', file_name)
                if re.search('[Ll]ists', file_name):
                    meta_open_name = re.sub('_', '-', file_name[9:]) + '-wiki-list.meta'
                else:
                    meta_open_name = re.sub('_', '-', file_name[8:]) + '-wiki-list.meta'
                #meta_open_name = re.sub('_', '-', file_name[8:]) + '-wiki-list.meta'
                if os.path.isfile(file_open_name):
                    for singer in singer_list:
                        match_num = re.match('\[\d+\]', singer)
                        if not match_num:
                            if singer not in open(file_open_name).read().decode('utf-8'):
                                with open(file_open_name, 'a') as f:
                                    f.write('\n' + str(singer).decode('utf-8'))
                else:
                    if slash_match:
                        file_open_name = re.sub('/', '_', file_open_name)
                    with open(file_open_name, 'w') as ff:
                        ff.write(subcat_page + '\n\n')
                    with open(file_open_name, 'a') as f:
                        for i in singer_list:
                            match_num = re.match('\[\d+\]', i)
                            if not match_num:
                                f.write(i.encode('utf-8') + '\n')
                chdir(cat_path + '\meta')
                '''with open(meta_open_name.lower(), 'w') as f:
                    f.write('<meta name="meta.' + re.sub('_', '-', file_name[8:].lower()) + '-wiki-list" lang="en"> \n')
                    for i in singer_list:
                        match_num = re.match('\[\d+\]', i)
                        if not match_num:
                            f.write('\n<pattern>' + i.encode('utf-8') + '</pattern>\n<velocity>\n\t#return("' + i.encode('utf-8') + '")\n</velocity>\n')
                    f.write('\n\n</meta>')'''

                #pathh = path + elem + '\\'
                pathh = path + 'Lists/' + cat_page_path + '/'
                fopenn = pathh + file_open_name
                fopen = open(fopenn, 'r').readlines()
                list_from_file = [re.sub('\n', '', i.decode('utf-8')) for i in fopen]
                with open(meta_open_name.lower(), 'w') as f:
                    f.write('<meta name="meta.' + re.sub('_', '-', file_name[8:].lower()) + '-wiki-list" lang="en"> \n')
                    for i in list_from_file:
                        match_num = re.match('\[\d+\]', i)
                        if not match_num:
                            try:
                                f.write('\n<pattern>' + i.encode('utf-8') + '</pattern>\n<velocity>\n\t#return("' + i.encode('utf-8') + '")\n</velocity>\n')
                            except UnicodeDecodeError:
                                f.write('\n<pattern>' + i.decode('utf-8') + '</pattern>\n<velocity>\n\t#return("' + i.decode('utf-8') + '")\n</velocity>\n')
                    f.write('\n\n</meta>')
                    
                print 'create meta file ' + meta_open_name.lower()
                            

            if int(len(singer_list)) > 0:
                print 'final singer_list len = ' + str(len(singer_list))
                print 'created ' + file_name + ' file'
         
            #print singer_list
            del singer_list[:]
            if cat_page in subcat_list:
                used_subcat_list.append(cat_page)
                subcat_list.remove(cat_page)
            if subcat_page in subcat_list:
                used_subcat_list.append(subcat_page)
                subcat_list.remove(subcat_page)
                #print 'cat removed ' + subcat_page
            print 'used_subcat_list length ' + str(len(used_subcat_list))
