#! /usr/bin/python3

# reads folder
# finds missing folders from last_done
# gets images, checks image types
# build markdown for entries
## TO DO:
# [X] find last entry for me
# [X] insert new entries in propper place
# [ ] insert docstrings as text on .md file
# [ ] use CL arguments to set tool
# [ ] use CL arguments to set Markdown comments
# [ ] use CL arguments to commit and push README.md
# [ ] Guard against malformed file names like sketch_2022_06_25..png


from os import listdir
from os.path import join, exists
from itertools import takewhile

from helpers import get_image_names

REPO_MAIN_URL = 'https://github.com/villares/sketch-a-day/tree/main'
# YEAR and base_path to sketch-a-day folder are set manually, hard-coded
YEAR = '2022'   
# base_path = "/Users/villares/sketch-a-day" # 01046-10 previously
base_path = '/home/villares/GitHub/sketch-a-day'
year_path = join(base_path, YEAR)

if not exists(year_path):
    sketch_folders = []  # for the benefit of next_day.py
    print(f"{__file__}: Couldn't find the sketch-a-day year folder!")
else:
    sketch_folders = listdir(year_path)
readme_path = join(base_path, 'README.md')

def most_recent_entry(readme_as_lines):
    entry_images = (
        line[line.find(YEAR) : line.find(']')]
        for line in readme_as_lines
        if '![' in line
    )
    try:
        return next(entry_images)[:10]
    except StopIteration:
        return 'Something wrong. No dated images found!'
    
def main():
    # open the readme markdown index
    with open(readme_path, 'rt') as readme:
        readme_as_lines = readme.readlines()
    # find date of the first image seen in the readme
    last_done = most_recent_entry(readme_as_lines)
    print('Last entry: ' + last_done)
    # find folders after the last_done one (folders start with ISO date)
    rev_sorted_folders = sorted(sketch_folders, reverse=True)
    not_done = lambda f: last_done not in f
    new_folders = [folder for folder in takewhile(not_done, rev_sorted_folders)]
    # find insertion point
    insert_point = 3 # in case lines is empty
    for insert_point, line in enumerate(readme_as_lines):
        if last_done in line:
            break
    # iterate on new folders
    for folder in reversed(new_folders):
        imgs = get_image_names(year_path, folder)
        # insert entry if matching image found
        for img in imgs:
            if img.split('.')[0].startswith(folder):
                entry_text = build_entry(folder, img)
                readme_as_lines.insert(insert_point - 3, entry_text)
                print('Adding: ' + folder)
                break
    # overwrite the readme markdown index
    with open(readme_path, 'wt') as readme:
        content = ''.join(readme_as_lines)
        readme.write(content)


def build_entry(folder, image_filename):
    """
    Return a string with markdown formated
    for the sketch-a-day index page entry
    of image (for a certain year).
    """
    tools = {
        'pde': '[[Processing Java](https://processing.org)]',
        'pyde': '[[Py.Processing](https://villares.github.io/como-instalar-o-processing-modo-python/index-EN)]',
        'flat': '[[Python + flat](https://xxyxyz.org/flat)]',
        'pyp5js': '[[pyp5js](https://berinhard.github.io/pyp5js/)]',
        'py5': '[[py5](https://py5coding.org/)]',
        'shoebot': '[[shoebot](http://shoebot.net/)]',
        'pyxel': '[[pyxel](https://github.com/kitao/pyxel/blob/master/README.md)]',
        'tk': '[tkinter]',
        'freecad': '[FreeCAD](https://freecadweb.org)'       
    }
    folder_path = join(year_path, folder)
    tools_mentioned = (t for t in tools.keys() if t in image_filename.lower())
    try:
        tool = next(tools_mentioned)
    except StopIteration:
        tool = 'py5'
        for f in listdir(folder_path):
            if 'pyde' in f:
                tool = 'pyde'
            elif 'pde' in f:
                tool = 'pde'
                
    docstring = search_docstring(folder_path)
    if docstring:
        comment = '\n\n' + docstring
    else:
        comment = ''
        
    link = f'{REPO_MAIN_URL}/{YEAR}/{folder}'
    
    return f"""
---

### {folder}

![{folder}]({YEAR}/{folder}/{image_filename})

[{folder}]({link}) {tools[tool]}{comment}
"""

def search_docstring(folder):
    print(listdir(folder))
    return None


if __name__ == '__main__':
    main()
