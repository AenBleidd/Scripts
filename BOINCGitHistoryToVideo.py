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

data_begin = 250
bar_begin = 450
bar_step = (width - bar_begin - 175) / 100

max_commits_str = run_command(f'git -C {repo} shortlog --summary --numbered --no-merges | head -n 1').split('\n')[0]
max_commits = int(max_commits_str.split()[0])

image_files = []

while cur_date < last_date:
    image = Image.new('RGBA', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    draw.text((135, 50), 'Top 25 contributors', fill='black', font=date_font)

    print(cur_date.strftime('%Y-%m-%d'))
    next_date = cur_date + datetime.timedelta(days=1)
    command = f'git -C {repo} shortlog --summary --numbered --no-merges --since={first_date.strftime('%Y-%m-%d')} --until={next_date.strftime('%Y-%m-%d')}'
    commits_by_author = []
    commits = run_command(command)
    i = 0
    for line in commits.split('\n'):
        if line.strip():
            parts = line.strip().split()
            num_commits = int(parts[0])
            author = ' '.join(parts[1:])
            commits_by_author.append({'author': author, 'commits': num_commits})
            draw.text((50, (i*40+50+(i*10))+data_begin), f'{author}', fill='black', font=data_font)
            draw.rectangle([bar_begin, i*40+50+(i*10)+data_begin, bar_begin + ((num_commits / max_commits) * 100 + 1) * bar_step, (i+1)*40+50+(i*10)+data_begin], fill=(0, 102, 255))
            draw.text((bar_begin + ((num_commits / max_commits) * 100 + 1) * bar_step + 10, (i*40+50+(i*10))+data_begin), f'{num_commits}', fill='black', font=data_font)
            i += 1
            if i >= 25:
                break

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
