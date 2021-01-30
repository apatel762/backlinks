import argparse
import os
import subprocess
from argparse import Namespace
from logging import Logger
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any, Union

import util


def main(notes_folder: str, temp_folder: str, html_folder: str) -> None:
    logger: Logger = util.get_logger(logger_name='pandocify')

    for folder in [notes_folder, temp_folder, html_folder]:
        logger.info('creating folder: "%s" if it doesn\'t exist already', folder)
        util.create_folder(folder)

    for file in os.listdir(notes_folder):
        if not util.is_md(file):
            continue

        # the path to the note is always gonna be in the notes_folder
        file_full_path: str = notes_folder + os.sep + file
        note_title = util.first_line(file_full_path)

        # the output HTML file should have the same name as the note but with
        # the .html suffix and it should be in the html folder
        file_html: str = html_folder + os.sep + file
        file_html: Path = Path(file_html)
        file_html: Path = file_html.with_suffix('')
        file_html: Path = file_html.with_suffix('.html')
        file_html: str = str(file_html)

        # the backlinks file should have the same name as the note but with
        # the .md.backlinks suffix, and it should be in the temp folder
        file_backlinks: str = temp_folder + os.sep + file + '.backlinks'

        logger.info('converting %s to html', file)
        # examples of using subprocess.run
        # https://www.programcreek.com/python/example/94463/subprocess.run
        run: Union[CompletedProcess[Any], CompletedProcess[bytes]] = subprocess.run(
            args=[
                'pandoc',
                f'"{file_full_path}"',
                f'"{file_backlinks}"',
                '--from=markdown',
                '--to=html5',
                f'--output="{file_html}"'
            ],
            env={
                'PATH': os.environ['PATH']
            },
            check=True,
            text=True
        )


if __name__ == '__main__':
    """
    arg parse:
      path to markdown notes
      relative path to folder where backlinks files will go
      relative path to folder where HTML files will go
    """
    parser = argparse.ArgumentParser(description='Convert markdown notes to HTML')
    parser.add_argument(
        '-n', '--notes',
        required=True,
        type=str,
        help='The absolute path of your notes folder')
    parser.add_argument(
        '-t', '--temp',
        required=True,
        type=str,
        help='The relative path of the \'temp\' folder where the backlinks files are. '
             'These files should be generated before running this script.')
    parser.add_argument(
        '-o', '--html',
        required=True,
        type=str,
        help='The relative path to the folder where HTML files will go')
    args: Namespace = parser.parse_args()

    main(notes_folder=args.notes, temp_folder=args.temp, html_folder=args.html)
