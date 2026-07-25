# pip install po-excel-translate

# from pathlib import Path
# import po_excel_translate as poet
#
# def po2xls(path):
# 	po_files_to_convert = [
# 		poet.PortableObjectFile(path)
# 	]
# 	poet.PortableObjectFileToXLSX(
# 		po_files=po_files_to_convert,
# 		comment_types=[poet.CommentType.SOURCE],
# 		output_file_path=Path("ro-example.xlsx")
# 	)
#
# def xls2po(path,path2):
# 	poet.XLSXToPortableObjectFile(
# 		locale="ru",
# 		input_file_path=Path(path),
# 		output_file_path=Path(path2)
# 	)
# # po2xls('/home/shapick/PycharmProjects/template/locales/en/LC_MESSAGES/bot_translate.po')
# xls2po('/home/shapick/PycharmProjects/template/other/ro-example.xlsx','/home/shapick/PycharmProjects/template/locales/en/LC_MESSAGES/bot_translate.po')
from __future__ import print_function
import re
import csv

def stripEnds(line):
    line = re.sub(r'^\n|\n$', ' ', line)
    line = line.replace('\\n', ' ')
    line = re.sub(r'\s+', ' ', line)
    line = re.sub(r'^[ ]|[ ]$', '', line)
    line = re.sub(r'^"|"$', '', line)
    return line

def exractVariables(line):
    line_vars = {}
    pattern = re.compile(r"%\(\w+\)s")
    items = re.findall(pattern, line)
    for i, item in enumerate(items):
        code = 'xxx' + str(i) + 'xxx'
        line = line.replace(item, code)
        line_vars[ code ] = item
    var_str = ', '.join(reversed(['%s=%s' % (c, v) for (c, v) in line_vars.items()]))
    return [line, var_str]

def po_to_scv(path_po, path_csv):
    string = ""
    with open(path_po) as f, open(path_csv, 'w') as c:
        writer = csv.writer(c)
        for i, line in enumerate(f, 1):
            if(line.startswith('#')):
                continue

            if(re.search('msgstr', line)): ## Line index found
                string = stripEnds(string)
                string,var_str = exractVariables(string)
                print (string, '>>>', var_str)
                writer.writerow((i, var_str, string))
            elif(line.startswith('msgid')):
                line = line.replace('msgid "', '')
                line = stripEnds(line)
                string = line
            else:
                line = stripEnds(line)
                string += " " + line




def decodeVars(line, var_dict, start_new_line, end_new_line):
    for (code,var) in var_dict.items():

        line = line.replace(code,var)
    return start_new_line + line + end_new_line

def scv_lto_po():
    with open("/home/shapick/PycharmProjects/template/locales/ru/LC_MESSAGES/bot_translate.po") as f, open("translations.csv") as c,open(   '/home/shapick/PycharmProjects/template/locales/en/LC_MESSAGES/bot_translate.po', 'w+') as d:
            # open('locale/ru/LC_MESSAGES/django.po', 'w+') as r,\
            # open( 'locale/ja/LC_MESSAGES/django.po', 'w+') as j,\
            # open('locale/zh/LC_MESSAGES/django.po', 'w+') as z,\
            # open(    'locale/pt/LC_MESSAGES/django.po', 'w+') as p:
        reader = csv.reader(c)
        f_ind = 1
        for row in reader:
            ind = int(row[0])
            var_dict = {x[0]: x[1] for x in [x.split("=") for x in row[1].split(", ")]} if ('=' in row[1]) else {}
            message = ''
            for i, line in enumerate(f, f_ind):
                if i == ind:

                    # print(row)
                    message = message.replace('"', '')

                    start_new_line = '\\n' if (re.match(r'^msgid[ ]*\\n[ ]*\S', message)) else ''
                    print(start_new_line)
                    end_new_line = '\\n' if (re.search(r'\S[ ]*\\n$', message)) else ''
                    # print('###', message)

                    # print('msgstr "' + decodeVars(row[3], var_dict, start_new_line, end_new_line) + '"', file=d)
                    # print('msgstr "' + decodeVars(row[4], var_dict, start_new_line, end_new_line) + '"', file=r)
                    # print('msgstr "' + decodeVars(row[5], var_dict, start_new_line, end_new_line) + '"', file=j)
                    # print('msgstr "' + decodeVars(row[6], var_dict, start_new_line, end_new_line) + '"', file=z)
                    # print('msgstr "' + decodeVars(row[7], var_dict, start_new_line, end_new_line) + '"', file=p)
                    break
                if (line.startswith('msgstr')):  ## Line index found
                    message = ''
                ln = line.strip()
                # print(line)
                # print( line.strip())
                message += ln
                # print(ln)
                # print(file=d)
                # print(ln, file=d)
                # print(ln, file=r)
                # print(ln, file=j)
                # print(ln, file=z)
                # print(ln, file=p)
            f_ind = i + 1
# scv_lto_po()
# po_to_scv("/home/shapick/PycharmProjects/template/locales/en/LC_MESSAGES/bot_translate.po", 'translations.csv')
def scv_to_po(path_po,path_csv,path_write):
    with open(path_po) as f, open(path_csv, 'r') as c, open(path_write, "w+") as d:
        reader = csv.reader(c)


        f_ind = 1

        message = ''
        for i, line in enumerate(f, f_ind):
            if (line.startswith('msgid')):

                k = line.replace('"', '')[6:].strip()
                for row in reader:
                    if row[2].strip() == k:
                        ln = row[3].strip()
                        message += ln
            else:
                ln = line.strip()
                message += ln

            # print()
            # print()
            # print()


            # ln = line.strip()
            # message += ln
        print(message)
        # f_ind = i + 1

            # print(message)


scv_to_po("/home/shapick/PycharmProjects/template/locales/ru/LC_MESSAGES/bot_translate.po", 'translations.csv', "/home/shapick/PycharmProjects/template/locales/en/LC_MESSAGES/bot_translate.po", )
