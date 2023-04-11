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

md_folder = Path(sys.argv[2]).parent.absolute()
md_files = list(md_folder.glob('*.md'))
md_files = [md_file.stem for md_file in md_files]
current_md_file = Path(sys.argv[2]).stem

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

        heading_patterns = [
            (r'={5}\s(.+)\s={5}', '#####'),
            (r'={4}\s(.+)\s={4}', '####'),
            (r'={3}\s(.+)\s={3}', '###'),
            (r'={2}\s(.+)\s={2}', '##'),
            (r'=\s(.+)\s=', '#'),
        ]

        for pattern, heading in heading_patterns:
            match = re.search(pattern, line)
            if match and not is_code_block and line.lstrip().startswith('='):
                line = f"{heading} {match.group(1)}\n"
                break

        if line.startswith('[[PageOutline'):
            continue
        if line == '[[TOC]]\n':
            continue
        if line.startswith('[=#'):
            continue
        if line == '\n' and not document_started:
            continue
        if line.lstrip().startswith('= ') and not document_started:
            line = line.replace('= ', '# ')
        if len(line):
            document_started = True

        match = re.findall(r'\s*\*\s[^\*]*', line)
        table_symbol = ''
        if len(match) == 1:
            table_symbol = '*'
        else:
            match = re.findall(r'\s*\-\s[^\-]*', line)
            if len(match) == 1:
                table_symbol = '-'
        if len(match) == 1 and is_code_block == False and table_symbol != '' and line.count(table_symbol) == 1 and line.lstrip().startswith(table_symbol):
            pos = line.find(table_symbol)
            if len(list_levels) == 0 or pos > list_levels[-1]:
                list_levels.append(pos)
            else:
                list_levels = list(filter(lambda x: x <= pos, list_levels))
            line = line.lstrip()
            line = " " * (len(list_levels) - 1) * 2 + line
        else:
            list_levels = []

        stripped = line.strip()

        match = re.search(r'(.*)::(.*)', line)
        if match and not is_code_block:
            if stripped != 'Email: daniel-monroe :: verizon net.' and match.group(2).startswith(' '):
                line = '### ' + match.group(1).strip() + '\n' + match.group(2).strip() + '\n'

        if stripped.endswith('::') and is_code_block == False:
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

        if line.strip() == '----' and is_code_block == False:
            line = '\n' + line
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
                is_code_block = False
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
            line = line.replace('<![CDATA[', '\\<![CDATA[')
            line = line.replace('&amp;', '\\&amp;')
            line = line.replace('&apos;', '\\&apos;')
            line = line.replace('&quot;', '\\&quot;')
            line = line.replace('&gt;', '\\&gt;')
            line = line.replace('&lt;', '\\&lt;')
            line = line.replace('CrossProjectId', 'CrossProjectUserId')
            if is_table == False:
                line = line.replace('[[BR]]', '\n\n')
                line = line.replace('[[br]]', '\n\n')
            else:
                line = line.replace('[[BR]]', '')
                line = line.replace('[[br]]', '')
            match = re.findall(r'(![\w]+[^!\s]+)', line)
            if match:
                for m in match:
                    line = line.replace(m, m[1:])
        url_replaced = False
        line = line.replace('[wiki:', '[')
        match = re.search('\[\[Image\((\S+),\s*(.+)\)\]\]', line)
        if match and url_replaced == False and not is_code_block:
            line = '![' + match.group(2) + '](' + match.group(1) + ')\n\n'
            url_replaced = True
        match = re.findall(r'(\[(\".*[^\,]\") ([^\]\[]*)\])', line)
        if not match:
            match = re.findall(r'(\[(\S*[^\,]) ([^\]\[]*)\])', line)
        if match and not is_code_block and url_replaced == False:
            for _, u, t in match:
                if u.strip() == '':
                    continue
                if t.find('..') != -1:
                    continue
                if u.startswith('//'):
                    url = u.replace('//', 'https://boinc.berkeley.edu/')
                else:
                    url = u
                url = url.replace('"', '')
                url = url.replace('\'', '')
                url_replace_list = ['DevProjects', 'Error', 'PrefsReference', 'Proposal', 'SourceCodeGit', 'test',
                                    'Translate', 'TroubleshootClient', 'Tutorial', 'WorkShop07', 'WorkShop08',
                                    'WorkShop09', 'WorkShop10', 'WorkShop11', 'WorkShop12', 'WorkShop13',
                                    'HackFest']
                for r in url_replace_list:
                    if url.startswith(r + '/'):
                        url = url.replace(r + '/', r + '_')
                        url = url.replace(' ', '')
                url = url.replace('\'', '')
                if url.startswith('source:boinc'):
                    url = url.replace('source:boinc', 'https://github.com/BOINC/boinc')
                url = url.replace('attachment:', '')
                url = url.replace('userw:', 'https://boinc.berkeley.edu/wiki/')
                url = url.replace('[', '')
                url = url.replace(']', '')
                if (url.find('UnixClient') != -1 and url.find('UnixClientPackage') == -1):
                    url = url.replace('UnixClient', 'UnixClientPackage')
                url = url.replace('ProjectMain', 'Home')
                text = t.replace('| ', '')
                line = line.replace('[' + u + ' ' + t + ']', '[' + text + '](' + url + ')')
                line = line.replace('[' + text + '](' + url + ')]', '[' + text + '](' + url + ')')
            url_replaced = True
        else:
            match = re.findall(r'attachment:(\S+)', line)
            if match and not is_code_block:
                for m in match:
                    line = line.replace('attachment:' + m, '[' + m + '](' + m + ')')
                url_replaced = True
        match = re.search('(.*)(http:\/\/folding\.stanford\.edu\/)(.*)', line)
        if match:
            line = match.group(1) + 'https://foldingathome.org/' + match.group(3) + '\n'
            url_replaced = True
        match = re.search('\[\[(.+)\((\S+)\)\]\]', line)
        if match and url_replaced == False:
            line = '![' + match.group(1) + '](' + match.group(2) + ')\n'
            url_replaced = True
        match = re.findall(r'\[\[(\S+)\]\]', line)
        if match and url_replaced == False:
            line = line.replace('[[' + match[0] + ']]', '[' + match[0] + '](' + match[0] + ')')
            url_replaced = True
        match = re.findall(r'\[(\w+)\][^(]', line)
        if match and not is_code_block and line.startswith('#') == False and url_replaced == False:
            url = match[0]
            if not re.search(r'(\d+)', url) and url != 'flavor':
                line = line.replace('[' + url + ']', '[' + url + '](' + url + ')')
                url_replaced = True
        match = re.findall(r'\[(http\S+)\][^(]', line)
        if match and not is_code_block and line.startswith('#') == False and url_replaced == False:
            line = line.replace('[' + match[0] + ']', '[' + match[0] + '](' + match[0] + ')')
            url_replaced = True
        line = line.replace('http://boinc.berkeley.edu', 'https://boinc.berkeley.edu')
        line = line.replace('https://boinc.berkeley.edu/trac/wiki/', '')

        if not is_code_block and not url_replaced and line.find('http') == -1 and line.find('ftp') == -1:
            line = line.replace('//', '*')

        match = re.findall(r'[^\`\\](<\S+\>)[^\`]', line)
        if match and not is_code_block:
            for m in match:
                line = line.replace(m, '\\' + m)

        for md_file in md_files:
            if md_file == 'Home':
                md_file = 'ProjectMain'
                md_replace = 'Home'
            else:
                md_replace = md_file
            if md_file != current_md_file and md_file != 'Home':
                match = re.search('[^\[\(\w]' + md_file + '[^\]\)\w]', line)
                if match and not is_code_block and url_replaced == False:
                    line = line.replace(md_file, '[' + md_file + '](' + md_replace + ')')

        if not waiting_for_code_language:
            output_file.write(line)
        else:
            buffer = line
