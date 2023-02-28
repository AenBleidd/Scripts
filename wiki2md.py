# This script converts BOINC wiki pages to markdown format
from pathlib import Path
import re
import sys

document_started = False
list_levels = []
is_table = False
is_pseudo_table = False
is_code_block = False
waiting_for_code_language = False
buffer = ''
is_comment = False

print('Converting ' + sys.argv[1] + ' to ' + sys.argv[2] + '...')


# read input file line by line and write to output file
with open(sys.argv[1], 'r', encoding='utf-8') as input_file, open(sys.argv[2], 'w', encoding='utf-8') as output_file:
    for line in input_file:
        line = line.rstrip() + '\n'
        stripped = line.strip()

        match = re.search('\#\!(\S*)', stripped)
        if match:
            if match.group(1) == 'comment' or match.group(1) == 'html':
                waiting_for_code_language = False
                buffer = ''
                is_comment = True
                line = ''
                stripped = ''
            if buffer != '':
                buffer = buffer.replace('```', '```' + match.group(1))
                line = buffer
            waiting_for_code_language = False
            buffer = ''
        else:
            if buffer != '':
                line = buffer + line
            waiting_for_code_language = False
            buffer = ''

        if stripped.startswith('||=') and stripped.endswith('=||'):
            is_table = True
            line = stripped
            columns = line.count('||') - 1
            line = line.replace('=||=', ' | ')
            line = line.replace('||=', '| ')
            line = line.replace('=||', ' |\n')
            line = '\n' + line
            for i in range(columns):
                line += '| --- '
            line += '|\n'
        elif stripped.startswith('||'):
            line = stripped
            if is_table == False:
                is_table = True
                if stripped.endswith('||'):
                    columns = line.count('||') - 1
                else:
                    columns = line.count('||')
                line = '\n'
                for i in range(columns):
                    line += '| <!-- --> '
                line += '|\n'
                for i in range(columns):
                    line += '| --- '
                line += '|\n'
                stripped = stripped.replace('||', '|')
                line += stripped + '\n'
            else:
                line += '\n'
        else:
            is_table = False

        match = re.search(r'=\s(.+)\s=', line)
        if match and is_code_block == False:
            line = '# ' + match.group(1) + '\n'
        if line.startswith('[[PageOutline'):
            continue
        if line == '[[TOC]]\n':
            continue
        if line == '\n' and not document_started:
            continue
        if len(line):
            document_started = True

        match = re.findall(r'\s*\*\s[^\*]*', line)
        if len(match) == 1 and is_code_block == False:
            pos = line.find('*')
            if len(list_levels) == 0 or pos > list_levels[-1]:
                list_levels.append(pos)
            else:
                list_levels = list(filter(lambda x: x <= pos, list_levels))
            line = line.lstrip()
            line = " " * (len(list_levels) - 1) + line
        else:
            list_levels = []

        match = re.search(r'={2}\s(.+)\s={2}', line)
        if match:
            line = '## ' + match.group(1) + '\n'
        stripped = line.strip()

        match = re.search(r'(.*)::(.*)', line)
        if match:
            if stripped != 'Email: daniel-monroe :: verizon net.' and match.group(2).startswith(' '):
                line = '### ' + match.group(1).strip() + '\n' + match.group(2).strip() + '\n'

        if stripped.endswith('::'):
            line = '### ' + stripped[:-2].rstrip() + '\n'
            is_pseudo_table = True
        else:
            if line.startswith('	') and is_code_block == False:
                line = line.lstrip()

            if line.startswith(' '):
                if is_pseudo_table:
                    line = line.lstrip()
            else:
                is_pseudo_table = False

        if line.startswith('\'\'\'') and line.endswith(' \'\'\'\n'):
            line = '**' + line[3:-5] + '**\n'

        line = line.replace('||', '|')
        line = line.replace('\'\'\'', '**')
        if line != '> SET PASSWORD FOR \'boincadm\'@\'localhost\'=\'\';\n':
            line = line.replace('\'\'', '*')

        if line.find('{{{') != -1:
            is_code_block = True
            waiting_for_code_language = True
            line = line.replace('{{{', '```')
        if line.find('}}}') != -1:
            if is_comment == True:
                is_comment = False
                continue
            is_code_block = False
            waiting_for_code_language = False
            line = line.replace('}}}', '```')
        if line.lstrip().startswith('<') and is_comment == True:
            continue
        line = line.replace('“', '"')
        line = line.replace('”', '"')
        line = line.replace(' ', " ")
        line = line.replace('’', "'")
        line = line.replace('​[', '[')
        if is_code_block == False:
            line = line.replace('<ended>', '\\<ended>')
            line = line.replace('</ended>', '\\</ended>')
            line = line.replace('<tab>', '\\<tab>')
            line = line.replace('<name>', '\\<name>')
            line = line.replace('</name>', '\\</name>')
            line = line.replace('<ngpus>', '\\<ngpus>')
            line = line.replace('</ngpus>', '\\</ngpus>')
            line = line.replace('<cuda/>', '\\<cuda/>')
            line = line.replace('<cal/>', '\\<cal/>')
            line = line.replace('<opencl/>', '\\<opencl/>')
            if is_table == False:
                line = line.replace('[[BR]]', '\n\n')
            else:
                line = line.replace('[[BR]]', '')
            match = re.findall(r'(![\w]+[^!\s]+)', line)
            if match:
                for m in match:
                    line = line.replace(m, m[1:])
        match = re.findall(r'(\[(\S*) ([^\]\[]*)\])', line)
        if match:
            for _, u, t in match:
                if u.strip() == '':
                    continue
                if t.find('..') != -1:
                    continue
                if u.startswith('//'):
                    url = u.replace('//', 'https://boinc.berkeley.edu/')
                else:
                    url = u
                url_replace_list = ['DevProjects', 'Error', 'PrefsReference', 'Proposal', 'SourceCodeGit', 'test',
                                    'Translate', 'TroubleshootClient', 'Tutorial', 'WorkShop07', 'WorkShop08',
                                    'WorkShop09', 'WorkShop10', 'WorkShop11', 'WorkShop12', 'WorkShop13',
                                    'HackFest']
                for r in url_replace_list:
                    if url.startswith(r + '/'):
                        url = url.replace(r + '/', r + '_')
                url = url.replace('\'', '')
                if url == 'source:boinc':
                    url = 'https://github.com/BOINC/boinc'
                line = line.replace('[' + u + ' ' + t + ']', '[' + t + '](' + url + ')')
                line = line.replace('userw:', '')
                line = line.replace('wiki:', '')
        match = re.search('(.*)(http:\/\/folding\.stanford\.edu\/)(.*)', line)
        if match:
            line = match.group(1) + 'https://foldingathome.org/' + match.group(3) + '\n'
        match = re.search('\[\[(.*)\((\S*)\)\]\]', line)
        if match:
            line = '![' + match.group(1) + '](' + match.group(2) + ')\n'
        match = re.findall(r'\[\[(\S*)\]\]', line)
        if match:
            line = line.replace('[[' + match[0] + ']]', '[' + match[0] + '](' + match[0] + ')')
        line = line.replace('http://boinc.berkeley.edu', 'https://boinc.berkeley.edu')
        line = line.replace('https://boinc.berkeley.edu/trac/wiki/', '')

        if not waiting_for_code_language:
            output_file.write(line)
        else:
            buffer = line