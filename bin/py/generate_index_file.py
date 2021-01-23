import argparse
import os
import pathlib
from typing import List, Tuple


def last_n_chars(s: str, n: int) -> str:
    return s[-n::]


def is_md(file_name: str) -> bool:
    return last_n_chars(file_name, n=3) == '.md'


def first_line(file_path: str) -> str:
    title = ''
    with open(file_path, 'r') as f:
        first_line = f.readline()
        title = first_line[2:]
    return title


def link_data(folder_path: str) -> List[Tuple[str, str]]:
    tmp = []
    for file_name in os.listdir(folder_path):
        if not is_md(file_name):
            continue

        title = first_line(folder_path + '/' + file_name)
        tmp.append((file_name, title))

    return tmp

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate an index file in HTML for other HTML files')
    parser.add_argument(
        'temp_folder', type=str,
        help='The relative path of the temp folder (where temporary files '
             'are left during the build)'
    )
    parser.add_argument(
        'notes_folder', type=str,
        help='The absolute path of your notes folder'
    )
    args = parser.parse_args()

    temp_folder = args.temp_folder
    notes_folder = args.notes_folder

    print(f'creating index.md in {temp_folder}')

    data = link_data(folder_path=notes_folder)

    with open(f'{temp_folder}/index.md', 'w') as f:
        f.write('# Index')
        f.write('\n')
        f.write(f'You have {len(data)} permanotes in your collection')
        f.write('\n')
        f.write('\n')
        for file_name, title in data:
            link = file_name.replace('.md', '.html')
            f.write(f'- [{title}]({link})\n')
