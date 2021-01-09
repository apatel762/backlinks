import argparse
import os
import pathlib
from html.parser import HTMLParser


def last_n_chars(s: str, n: int) -> str:
    return s[-n::]


def is_html(file_name: str) -> bool:
    return last_n_chars(file_name, n=5) == '.html'


def first_line(file_path: str) -> str:
    title = ''
    with open(file_path, 'r') as f:
        first_line = f.readline()
        title = first_line[2:]
    return title


def markdown_link(link: str, display: str) -> str:
    return f'[{display}]({link})'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate an index file in HTML for other HTML files')
    parser.add_argument(
        'html_folder', type=str,
        help='The relative path of the folder where you are keeping your '
             'HTML files (the ones that you want the index file for).'
    )
    parser.add_argument(
        'notes_folder', type=str,
        help='The absolute path of your notes folder'
    )
    args = parser.parse_args()

    html_folder = args.html_folder
    notes_folder = args.notes_folder
    html_files = [fn for fn in os.listdir(html_folder) if is_html(file_name=fn)]

    print('creating index file...')
    print(f'found {len(html_files)} html files to index')

    with open(f'{html_folder}/index.html', 'w') as f:
        f.write(' Index')
        f.write(f'There are {len(html_files)} permanotes in your collection:')
        f.write('')
        for file_name in html_files:
            link_display = first_line(file_path=f'{html_folder}/{file_name}')
            link: str = markdown_link(link=file_name, display=link_display)
            f.write(f'- {link}')