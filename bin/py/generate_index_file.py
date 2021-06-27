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


def todo_data(folder_path: str) -> List[Tuple[str, List[str]]]:
    tmp = []
    for file_name_ in os.listdir(folder_path):
        if not util.is_md(file_name_):
            continue

        todos: List[str] = util.extract_todos(util.path(folder_path, file_name_))
        if len(todos) > 0:
            tmp.append((file_name_, todos))

    return tmp


def create_index_file(temp_folder: str, notes_folder: str):
    logger: Logger = util.get_logger(logger_name='generate_index_file')

    data: List[Tuple[str, str]] = link_data(folder_path=notes_folder)
    todos: List[Tuple[str, List[str]]] = todo_data(folder_path=notes_folder)

    logger.info(f'creating index.md in {temp_folder}')
    for file_name, title in data:
        if file_name == 'index.md':
            logger.warning('aborting, you have a custom index.md in your notes')
            sys.exit(0)

    with open(f'{temp_folder}/index.md', 'w') as f:
        f.write('# Home')
        f.write('\n')
        f.write('\n')

        # write out the ::to-do:: items if there are any in the notes
        if len(todos) > 0:
            f.write('## Tasks')
            f.write('\n')
            f.write('\n')
            f.write(f'A task list (also called a to-do list or "things-to-do") is a '
                    f'list of tasks to be completed, such as chores or steps toward '
                    f'completing a project. It is an inventory tool which serves as an '
                    f'alternative or supplement to memory.')
            f.write('\n')
            f.write('\n')
            f.write('Wikipedia. "[Time management]('
                    'https://en.wikipedia.org/wiki/Time_management'
                    '#Implementation_of_goals)". *[Archived]('
                    'https://web.archive.org/web/20210627141229/https://en.wikipedia'
                    '.org/wiki/Time_management)*. Retrieved June 27, 2021.')
            f.write('\n')
            f.write('\n')
            f.write('<details>')
            f.write('<summary>Click to expand!</summary>')
            for file_name, list_of_todos_in_file in todos:
                link = util.change_file_extension(file_name, '.html')
                for todo in list_of_todos_in_file:
                    f.write(f'- [X]({link}) - {todo}')
                    f.write('\n')
            f.write('</details>')
            f.write('\n')
            f.write('\n')
            f.write('When you\'re done with a task, delete the todo item from the file '
                    'that you found it in so that it stops appearing here.')
            f.write('\n')
            f.write('\n')

        # write out a list of every notes in the folder
        f.write('## Notes')
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

    create_index_file(
        temp_folder=args.temp,
        notes_folder=args.notes)

