import argparse
import os
from logging import Logger
from typing import List, Tuple
import sys

import util


def link_data(folder_path: str) -> List[Tuple[str, str]]:
    tmp = []
    for file_name_ in os.listdir(folder_path):
        if not util.is_md(file_name_):
            continue

        note_title = util.note_title(util.path(folder_path, file_name_))
        tmp.append((file_name_, note_title))

    tmp.sort(key=lambda pair: os.path.getmtime(util.path(folder_path, pair[0])),
             reverse=True)
    return tmp


def create_index_files(temp_folder: str, notes_folder: str):
    logger: Logger = util.get_logger(logger_name='generate_index_file')

    data = link_data(folder_path=notes_folder)

    logger.info(f'creating index.md in {temp_folder}')
    for file_name, title in data:
        if file_name == 'index.md':
            logger.warning('aborting, you have a custom index.md in your notes')
            sys.exit(0)

    with open(f'{temp_folder}/index.md', 'w') as f:
        f.write('# Index')
        f.write('\n')
        f.write('\n')
        f.write(f'You have {len(data)} permanotes in your collection.')
        f.write('\n')
        f.write('\n')

        for file_name, title in data:
            link = util.change_file_extension(file_name, '.html')
            f.write(f'- [{title}]({link})')
            f.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate an index file in HTML for other HTML files')
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
    args = parser.parse_args()

    create_index_files(
        temp_folder=args.temp,
        notes_folder=args.notes)

