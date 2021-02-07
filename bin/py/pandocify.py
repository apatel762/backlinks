import argparse
import os
from argparse import Namespace
from logging import Logger

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
        file_full_path: str = util.path(notes_folder, file)
        note_title = util.note_title(file_full_path)

        # the output HTML file should have the same name as the note but with
        # the .html suffix and it should be in the html folder
        file_html: str = util.path(html_folder, file)
        file_html: str = util.change_file_extension(file_html, '.html')

        # the backlinks file should have the same name as the note but with
        # the .md.backlinks suffix, and it should be in the temp folder
        file_backlinks: str = util.path(temp_folder, file + '.backlinks')

        logger.info('converting %s to html (title=%s)', file, note_title)
        util.run(cmd=[
            'pandoc',
            file_full_path, file_backlinks,
            '--from=markdown',
            '--to=html5',
            '--no-highlight',
            f'--id-prefix={util.to_footnote_id(file)}',
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
