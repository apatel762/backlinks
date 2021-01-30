import argparse
import os
import subprocess
from argparse import Namespace
from logging import Logger
from pathlib import Path

import util


def get_lua_filter() -> str:
    """
    TODO: make this a bit more robust... what if the file doesn't exist
     same for all of the other similar functions below
    """
    return util.path('bin', 'links_to_html.lua')


def get_meta_html() -> str:
    return util.path('bin', 'meta', 'meta.html')


def get_before_body_html() -> str:
    return util.path('bin', 'meta', 'meta-before-body.html')


def get_after_body_html() -> str:
    return util.path('bin', 'meta', 'meta-after-body.html')


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
        note_title = util.note_title(file_full_path)

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

        logger.info('converting %s to html (title=%s)', file, note_title)
        util.run(cmd=[
            'pandoc',
            file_full_path, file_backlinks,
            '--from=markdown',
            '--to=html5',
            f'--output={file_html}',
            f'--lua-filter={get_lua_filter()}',
            f'--include-in-header={get_meta_html()}',
            f'--metadata=pagetitle:{note_title}',
            f'--include-before-body={get_before_body_html()}',
            f'--include-after-body={get_after_body_html()}'
        ])


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
