# pip install pillow
# pip install moviepy

import datetime
import subprocess

from moviepy import ImageSequenceClip
from PIL import Image, ImageDraw, ImageFont

repo = '../boinc/'
logo = '../boinc/clientgui/res/templates/icons/References/boinc_logo.png'

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, _ = process.communicate()
    return out.decode('utf-8')

first_date_str = run_command(f'git -C {repo} log --reverse --pretty=format:"%ad" --date=short').split('\n')[0]
first_date = datetime.datetime.strptime(first_date_str, '%Y-%m-%d')
today = datetime.datetime.now()
last_date = today + datetime.timedelta(days=1)

cur_date = first_date
width = 1080
height = 1920

data_font = ImageFont.truetype('l_10646.ttf', 35)
date_font = ImageFont.truetype('impact.ttf', 100)

log_output = run_command(f'git -C {repo} log --no-merges --reverse --pretty=format:"%H %ad" --date=short --shortstat')

commits = []
data = {}
lines = log_output.split('\n')
i = 0
while i < len(lines):
    if lines[i].strip():
        parts = lines[i].split()
        commit_hash = parts[0]
        commit_date = parts[1]
        lines_added = 0
        lines_deleted = 0
        if i + 1 < len(lines) and ('files changed' in lines[i + 1]) or ('file changed' in lines[i + 1]):
            stats = lines[i + 1].split(',')
            for stat in stats:
                if ('insertions' in stat or 'insertion' in stat):
                    lines_added = int(stat.strip().split()[0])
                if ('deletions' in stat or 'deletion' in stat):
                    lines_deleted = int(stat.strip().split()[0])
            i += 1
        commits.append({
            'hash': commit_hash,
            'date': commit_date,
            'lines_added': lines_added,
            'lines_deleted': lines_deleted
        })
        diff = lines_added - lines_deleted
        if (commit_date in data.keys()):
            data[commit_date] += diff
        else:
            data[commit_date] = diff
    i += 1

data_final = {}
total_lines = 0
while cur_date < last_date:
    cur_date_key = cur_date.strftime('%Y-%m-%d')
    if cur_date_key in data.keys():
        total_lines += data[cur_date_key]
    else:
        total_lines += 0
    data_final[cur_date_key] = total_lines
    next_date = cur_date + datetime.timedelta(days=1)

    cur_date += datetime.timedelta(days=1)

max_value = max(data_final.values()) if data_final else 0

image_files = []
cur_date = first_date
left = 50
top = 250
right = width - left
bottom = height - 400
hor_step = (right - left) / len(data_final.keys())
ver_step = (bottom - top) / max_value
while cur_date < last_date:
    print(cur_date.strftime('%Y-%m-%d'))
    temp_date = first_date

    image = Image.new('RGBA', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    draw.text((270, 50), 'Lines of code', fill='black', font=date_font)

    i = 0
    while temp_date <= cur_date:
        draw.rectangle([left+i*hor_step, bottom-data_final[temp_date.strftime('%Y-%m-%d')]*ver_step, left+(i+1)*hor_step, bottom], fill=(0, 102, 255))
        temp_date += datetime.timedelta(days=1)
        i += 1
    value = data_final[cur_date.strftime('%Y-%m-%d')]
    draw.text((135, bottom + 10), f'{value:,}', fill='black', font=date_font)
    draw.text((50, 1680), f'{cur_date.strftime('%m.%Y')}', fill='black', font=date_font)
    logo_img = Image.open(logo).convert('RGBA')
    logo_img = logo_img.resize((384, 159))
    image.paste(logo_img, (width - 384 - 50, height - 159 - 100), logo_img)

    image_path = f'images/{cur_date.strftime('%Y-%m-%d')}.png'
    image.save(image_path)
    image_files.append(image_path)

    cur_date += datetime.timedelta(days=1)

clip = ImageSequenceClip(image_files, fps=60)
clip.write_videofile('output.mp4', codec='libx264')
