import argparse
import os
from logging import Logger
from typing import List, Tuple

import util


def link_data(folder_path: str) -> List[Tuple[str, str]]:
    tmp = []
    for file_name_ in os.listdir(folder_path):
        if not util.is_md(file_name_):
            continue

        note_title = util.first_line(folder_path + '/' + file_name_)
        tmp.append((file_name_, note_title))

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
    logger: Logger = util.get_logger(logger_name='generate_index_file')

    temp_folder = args.temp_folder
    notes_folder = args.notes_folder

    logger.info(f'creating index.md in {temp_folder}')

    data = link_data(folder_path=notes_folder)

    with open(f'{temp_folder}/index.md', 'w') as f:
        f.write('# Index')
        f.write('\n')
        f.write(f'You have {len(data)} permanotes in your collection.')
        for file_name, title in sorted(data, reverse=True):
            if file_name == 'now.md':
                f.write(' ')
                f.write('A good place to start would be at the ')
                f.write(f'[{title}]({file_name}) page.')
        f.write('\n')
        f.write('\n')
        for file_name, title in sorted(data, reverse=True):
            if file_name == 'now.md':
                continue
            link = file_name.replace('.md', '.html')
            f.write(f'- [{title}]({link})\n')
