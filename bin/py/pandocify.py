import argparse
import os
from argparse import Namespace
from logging import Logger
from pathlib import Path

import util


def main(notes_folder: str, temp_folder: str, html_folder: str) -> None:
    logger: Logger = util.get_logger(logger_name='pandocify')

    logger.info('notes_folder: %s', notes_folder)
    logger.info('temp_folder: %s', temp_folder)
    logger.info('html_folder: %s', html_folder)

    # for filename in os.listdir(notes_folder):
    #     if not util.is_md(filename):
    #         continue
    #
    #     path_to_note: Path = Path(notes_folder + '/' + filename)
    #     filename_html = str(Path(filename).with_suffix('').with_suffix('html'))
    #
    #     note_title = util.first_line(notes_folder + '/' + filename)
    #     output_filename = f"{html_folder}/{filename.replace('.md', '.html')}"
    #     util.convert_to_html(
    #         output_filename,
    #         notes_folder + '/' + filename,
    #
    #     )

    # for each file in the notes folder
    # convert it (& the corresponding backlinks file) using pandoc
    # the result must go to the html folder


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
