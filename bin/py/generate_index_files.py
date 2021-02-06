import argparse
import os
from logging import Logger
from typing import List, Tuple
import sys
import json

import util


def link_data(folder_path: str) -> List[Tuple[str, str]]:
    tmp = []
    for file_name_ in os.listdir(folder_path):
        if not util.is_md(file_name_):
            continue

        note_title = util.note_title(folder_path + '/' + file_name_)
        tmp.append((file_name_, note_title))

    return tmp


def create_json_index(note_data: List[Tuple[str, str]], destination_dir: str):
    # https://lunrjs.com/guides/index_prebuilding.html
    # the dictionary/json should be formatted as in that link so that it will
    # work as an index
    with open(util.path(destination_dir, 'index.json'), 'w') as json_file:
        json.dump(
            [
                {
                    'href': util.change_file_extension(file_name, '.html'),
                    'title': title
                }
                for file_name, title in note_data
            ],
            json_file)


def create_index_files(temp_folder: str, notes_folder: str, json_index_folder: str):
    logger: Logger = util.get_logger(logger_name='generate_index_file')

    data = link_data(folder_path=notes_folder)

    logger.info(f'creating index.json in {json_index_folder}')
    create_json_index(note_data=data, destination_dir=json_index_folder)

    logger.info(f'creating index.md in {temp_folder}')
    for file_name, title in sorted(data, reverse=True):
        if file_name == 'index.md':
            logger.info('aborting! you already have an index.md')
            sys.exit(0)

    with open(f'{temp_folder}/index.md', 'w') as f:
        f.write('# Index')
        f.write('\n')
        f.write(f'You have {len(data)} permanotes in your collection.')
        f.write('\n')
        f.write('\n')
        for file_name, title in sorted(data, reverse=True):
            link = file_name.replace('.md', '.html')
            f.write(f'- [{title}]({link})\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate an index file in HTML for other HTML files and '
                    'generate the index.json for searching through the site '
                    'using lunr.js')
    parser.add_argument(
        '-t', '--temp',
        required=True,
        type=str,
        help='The relative path of the temp folder (where temporary files '
             'are left during the build)')
    parser.add_argument(
        '-n', '--notes',
        required=True,
        type=str,
        help='The absolute path of your notes folder')
    parser.add_argument(
        '-j', '--json',
        required=True,
        type=str,
        help='The relative path of where the JSON index file will go')
    args = parser.parse_args()

    create_index_files(
        temp_folder=args.temp,
        notes_folder=args.notes,
        json_index_folder=args.json)

