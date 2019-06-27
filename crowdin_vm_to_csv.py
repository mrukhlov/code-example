import os
import fnmatch
import shutil
import re
from os import rename, listdir
import sys

reload(sys)
sys.setdefaultencoding('utf8')

end = '#end'
tab = '\t'
double_tab = '\t\t'
randomm = '#random\(\)'
macro_name = '#macro\((.*)\)'
new_stroke = '^\n$'
descr = '##\s+(.*)'
commented_macro = '###macro'

work_string = ''
rec = False
rec_init = False
first_run_check = True
first_input_check = False
descr_found = False
comment_found = False
use_buffer = False

os.chdir('E:\\test')
path_input = 'E:\\test\\SmallTalkAppraisalYouAreAwesome.vm'
path_output = 'E:\\test\\SmallTalkAppraisalYouAreAwesome.csv'
test_num = 0
with open(path_input, 'r') as f:
    #print f.readlines()
    for string in f.readlines():
        #clean(string))

        tab_match = re.search(tab, string)
        if tab_match:
            string = re.sub(tab, '', string)

        random = re.search(randomm, string)
        if random:
            string = re.sub(randomm, '', string)

        double_tab_match = re.search(tab, string)
        if double_tab_match:
            string = re.sub(double_tab, '', string)

        end_match = re.search(end, string)
        if end_match:
            string = re.sub(end, '', string)

        new_stroke = ('^\n$', string)
        if new_stroke:
            string = re.sub('^\n$', '', string)

        commented_macro_search = re.match('###macro', string)
        descr = re.search('##\s*(.+)', string)

        '''if comment_found != True:
            if not commented_macro_search:
                if descr:
                    description = descr.group(1)
                    #print description
            elif commented_macro_search:
                comment_found = True
                description = ''
        else:
            if descr:
                buffer_descr = descr.group(1)
                #print buffer_descr'''

        if comment_found != True:
            if not commented_macro_search:
                if descr:
                    descr_found = True
                    first_input_check = True
                    description = descr.group(1)
                    if rec == False:
                        rec = True
                    else:
                        rec = False
                    comment_found = False
            elif commented_macro_search:
                comment_found = True
                description = ''
        else:
            if descr:
                buffer_descr = descr.group(1)

        macro_name = re.match('#macro\((.*)\)', string)
        if macro_name:
            first_input_check = True
            string = re.sub('#macro\((.*)\)', macro_name.group(1), string)

            new_stroke_end = re.search('\n$', string)
            if new_stroke_end:
                string = re.sub('\n$', '', string)

            macro_name = string
            if rec == False:
                rec = True
            else:
                rec = False

            if comment_found == True:
                use_buffer = True
                comment_found = False
            #print macro_name

        if not macro_name and not descr:
            new_stroke_end = re.search('\n$', string)
            if new_stroke_end:
                string = re.sub('\n$', '', string)
            double_qoute = re.search('"', string)
            if double_qoute:
                string = re.sub('"', '\'', string)
            if new_stroke_end:
                string = re.sub('\n$', '', string)
            input = string
            descr_found = False

        #descr_check = False
        if rec == True:
            if descr:
                first_input_check = True
                if first_run_check == True:
                    work_string += '"' + description + '",'
                    first_run_check = False
                else:
                    work_string += '"\n' + '"' + description + '",'
                print work_string
            elif macro_name:
                if use_buffer == True:
                    work_string = buffer_descr + ' ' + macro_name
                    use_buffer = False
                elif descr_found == True:
                    work_string += ' "' + macro_name + '", "'
                elif descr_found == False:
                    work_string += '"\n"", "' + macro_name + '", "'
                print work_string
            elif not macro_name and not descr and len(string) > 0:
                if first_input_check == True:
                    work_string += string
                    first_input_check = False
                elif first_input_check == False:
                    work_string += '/n' + string
                #print work_string

        if rec == False:
            if descr:
                first_input_check = True
                work_string += '"\n' + '"' + description + '",'
                print work_string
            elif macro_name:
                if use_buffer == True:
                    work_string = buffer_descr + ' ' + macro_name
                elif descr_found == True:
                    work_string += ' "' + macro_name + '", "'
                elif descr_found == False:
                    work_string += '"\n"", "' + macro_name + '", "'
                print work_string
            elif not macro_name and not descr and len(string) > 0:
                if first_input_check == True:
                    work_string += string
                    first_input_check = False
                elif first_input_check == False:
                    work_string += '/n' + string
                #print work_string

        description = ''
        macro_name = ''
        string =''

#work_string = work_string + '"'

with open(path_output, 'w') as f:
    f.write(str(work_string))

'''li = ['smalltalk-agent-areyoubusy-data.ling', 'smalltalk-agent-areyouok-data.ling']
path = 'C:\\Workspace\\max-smalltalk\\ling\\en\\smalltalk'

for file_list in li:
    for d, dir, files in os.walk(path):
            for f in files:
                    if fnmatch.fnmatch(f, file_list):
                            dest_path = os.path.join(d,f)
                            print dest_path'''