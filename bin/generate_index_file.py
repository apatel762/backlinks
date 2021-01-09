import argparse
import os
import pathlib


def last_n_chars(s: str, n: int) -> str:
    return s[-n::]


def is_html(file_name: str) -> bool:
    return last_n_chars(file_name, n=5) == '.html'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate an index file in HTML for other HTML files')
    parser.add_argument(
        'html_folder', type=str,
        help='The relative path of the folder where you are keeping your '
             'HTML files (the ones that you want the index file for).'
    )
    args = parser.parse_args()

    html_folder = args.html_folder
    html_files = [fn for fn in os.listdir(html_folder) if is_html(file_name=fn)]

    for s in html_files:
        print(s)