import urllib
from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
import mechanize
from mechanize import Browser
import requests
import re
import os

#def getting_links():
link = 'http://rtw.ml.cmu.edu/rtw/kbbrowser/ontology.php'
pageFile = urllib.urlopen(link).read()
soup = BeautifulSoup(pageFile)

link_raw_list = []
for li in soup.select('html > body > ul'):
    for lii in li.find_all("a"):
        link_raw_list.append(lii)

link_list_backup = []
link_list = []
for w in link_raw_list:
    match = re.match('<a name=".*"></a>', str(w))
    if match:
        link_raw_list.remove(w)
        
for w in link_raw_list:
    replaced = re.sub('<a href="\.', 'http://rtw.ml.cmu.edu/rtw/kbbrowser', str(w))
    link_list_backup.append(replaced)
    
for w in link_list_backup:
    replaced = re.sub('" target="_top">.*</a>', '', w)
    link_list.append(replaced)
          
path = 'M:\\'
os.chdir(path)
with open('nell_links.txt', "w") as f:
    for i in link_list:
        f.write("%s\n" % i)

content_list = []
for i in link_list:
    replaced = re.sub('pred:', 'list.php?pred=', str(i))
    content_list.append(replaced)
    
print 'done'

#def links_iterate(link_list):

for i in content_list:
    link = i
    link_category = link[50:]
    next_link = 'http://rtw.ml.cmu.edu/rtw/kbbrowser/list.php?pred=%s&start=5000' % link_category

    link_map = '<a href="./map:%s" target="_top">map</a>' % link_category
    link_metadata = '<a href="./predmeta:%s" target="_top">metadata</a>' % link_category
    link_page1 = '<a href="./pred:%s&amp;start=0" target="_top">1</a>' % link_category
    link_page2 = '<a href="./pred:%s&amp;start=5000" target="_top">2</a>' % link_category
    link_page3 = '<a href="./pred:%s&amp;start=10000" target="_top">3</a>' % link_category
    link_instance = '<a href="./pred:%s&amp;list_sort=name" target="_top">instance</a>' % link_category
    link_iteration = '<a href="./pred:%s&amp;list_sort=iter" target="_top">iteration</a>' % link_category
    link_date = '<a href="./pred:%s&amp;list_sort=date" target="_top">date learned</a>' % link_category
    link_category_filter = '<a href="./pred:%s&amp;list_sort=prob" target="_top">confidence</a>' % link_category
    tr_prologue = '<tr class="prolouge">'
    tr_heading = '<tr class="heading">'
    link_filter_list = [link_map, link_metadata, link_page1, link_page2, link_page3, link_instance, link_iteration, link_date, link_category_filter, tr_prologue, tr_heading]

    prev_match = '<a href="\./pred:%s&amp;start=\d+" target="_top">prev</a>' % link_category
    sort_match = '<a href="\./pred:%s&amp;start=\d+&amp;list_sort=.*" target="_top">.*</a>' % link_category

    pageFile = urllib.urlopen(link).read()
    soup = BeautifulSoup(pageFile)

    site = soup.select('html > body > table')
    match = re.search('\d+[,.]*\d* instances', str(site))
    if match:
        found = match.group(0)
        match = re.search('\d+[,.]*\d*', found)
        instances_num = int(re.sub(',', '', match.group(0)))
        
    if instances_num > 0:
        table_raw_list = []
        for li in soup.select('html > body > table'):
            for lii in li.find_all("tr"):
                match = re.match('<tr class="prolouge">', str(lii))
                if match:
                    match_pl = re.search('\d+ pages', str(lii))
                    match = re.search('\d+ page', str(lii))
                    if match or match_pl:
                        found = match.group(0)
                        match = re.search('\d+', found)
                        pages_num = match.group(0)
                        

        for li in soup.select('html > body > table'):
            for lii in li.find_all("tr"):
                match = re.match('<tr class="prolouge">', str(lii))
                match1 = re.match('<tr class="heading">', str(lii))
                if not match and not match1:
                    table_raw_list.append(str(lii))

        iter_num = int(pages_num) - 1
        if iter_num > 0:
            link_words_q = 5000
            while iter_num != 0:
                next_link = 'http://rtw.ml.cmu.edu/rtw/kbbrowser/list.php?pred=%s&start=%s' % (link_category, link_words_q)
                pageFile = urllib.urlopen(next_link).read()
                soup = BeautifulSoup(pageFile)
                for li in soup.select('html > body > table'):
                    for lii in li.find_all("tr"):
                        match = re.match('<tr class="prolouge">', str(lii))
                        match1 = re.match('<tr class="heading">', str(lii))
                        if not match and not match1:
                            table_raw_list.append(str(lii))
                iter_num -= 1
                link_words_q += 5000

        table_raw_list_a = []
        table_raw_list_b = []
        table_raw_list_c = []
        table_raw_list_d = []
        table_raw_list_e = []
        table_list_list = [table_raw_list_a, table_raw_list_b, table_raw_list_c]

        temp_re = '<tr class="instance" id="0"><td class="instance"><a class="entls" href="\./.*:'
        temp_re1 = '" id="entls-\d+" target="_top">.*</a></td><td class="field">\d+</td><td class="field">.*</td><td class="field">'
        temp_re2 = '</td></tr>'
        temp_re3 = '_'
        temp_re4 = '\(Seed\) '
        re_list = [temp_re, temp_re1, temp_re2]

        for i in table_raw_list:
            replaced = re.sub(temp_re, '', i)
            table_raw_list_a.append(replaced)
        for i in table_raw_list_a:
            replaced = re.sub(temp_re1, ' => confidence ', i)
            table_raw_list_b.append(replaced)
        for i in table_raw_list_b:
            replaced = re.sub(temp_re2, '', i)
            table_raw_list_c.append(replaced)
        for i in table_raw_list_c:
            replaced = re.sub(temp_re3, ' ', i)
            table_raw_list_d.append(replaced)
        for i in table_raw_list_d:
            replaced = re.sub(temp_re4, ' ', i)
            table_raw_list_e.append(replaced)

        path = 'M:\\junk'
        os.chdir(path)
        with open(link_category + '_table.txt', "w") as f:
            for i in table_raw_list_e:
            #for i in table_raw_list:
                f.write("%s\n" % i)
        print 'finished ' + link_category
    else:
        print 'common page ' + link_category

source_path = 'E:\\junk\\'
list_path = 'C:\\Workspace\\dev-maxim\\meta\\en\\language\\list\\nell_lists'

for root, dirnames, filenames in os.walk(source_path):
    for i in filenames:
        meta_name = i.split('_')[0] + '-full-list.meta'
        file_open_path = source_path + i
        file_open = open(file_open_path, 'r')

        a = []
        with file_open as f:
            lines = f.read().splitlines()
            for i in lines:
                match = re.search(' => confidence.*\d+[,.]*\d*', str(i))
                if match:
                    sub = re.sub(' => confidence.*\d+[,.]*\d*', '', str(i))
                    a.append(sub)
        b = []
        for i in a:
            sub = re.sub('  ', ' ', str(i))
            b.append(sub)


        try:
            os.chdir(list_path)
        except(WindowsError):
            os.makedirs(list_path)
   
        with open(meta_name, "w") as f: 
            f.write('<meta name="meta.' + i.split('_')[0] + '-full-list" lang="en"> \n')

        with open(meta_name, "a") as f: 
            for i in b:
                f.write('\n<pattern>' + i + '</pattern>\n<velocity>\n\t#return("' + i + '")\n</velocity>\n')

        with open(meta_name, "a") as f: 
            f.write('\n\n</meta>')
