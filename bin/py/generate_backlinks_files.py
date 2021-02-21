import argparse
import os
import re
from logging import Logger
from typing import List, Tuple

# regular expression for finding markdown style links
# i.e. something like `[My Link](https://broadsilver.com)`
import util

# noinspection RegExpRedundantEscape
md_links = re.compile("\[(.*?)\]\((.*?)\)", re.DOTALL)


def markdown_filenames(folder_path: str) -> List[str]:
    return [fn for fn in os.listdir(folder_path) if util.is_md(fn)]


def html_link(href: str, display: str) -> str:
    # for some reason pandoc doesn't change the .md to .html in backlinks
    # so the replacement here is a little hack to make it work
    return f'<a href="{href.replace(".md", ".html")}">{display}</a>'


def backlinks_html(refs: List[Tuple[str, str]]) -> str:
    if len(refs) <= 0:
        return ''

    txt: List[str] = [
        '<div class="footer">',
        '<ul>'
    ]
    for backlink, link_display in set(refs):
        txt.append('<li>' + html_link(backlink, link_display) + '</li>')
    txt.append('</ul>')
    # we don't close the div.footer that we opened here; pandoc will do that
    # for us when it generates the final HTML. Why do this? so when pandoc
    # generates the footnotes, they will be included in the nicely formatted
    # footer section that we've created for the backlinks
    return '\n'.join(txt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate backlinks for files in a given folder')
    parser.add_argument(
        'notes_folder', type=str,
        help='The absolute path of the folder that holds all of your notes. '
             'All of the notes that you want to generate the backlinks for '
             'should be in the top-level of this folder; the script will not '
             'recursively serach for any markdown files that are in '
             'subfolders.')
    parser.add_argument(
        'temp_folder', type=str,
        help='The relative path of a folder where you want the backlinks '
             'files to be stored when they are generated.'
    )
    args = parser.parse_args()
    logger: Logger = util.get_logger(logger_name='generate_backlinks_files')

    notes_folder = args.notes_folder
    backlinks_folder = args.temp_folder

    file_names = markdown_filenames(folder_path=notes_folder)
    logger.info(f'Found {len(file_names)} files in {notes_folder}')

    util.create_folder(location=backlinks_folder)
    logger.info(f'Will put backlinks into: {backlinks_folder}/')

    # NOTE: current backlink searching is slow... O(n^2)
    for file_name in file_names:
        # a list of all of the files that reference this one
        references = []

        # look in all of the other files for references and put them in the
        # above list if we find any
        for other_file in file_names:
            if other_file == file_name:
                continue
            if other_file == 'index.md':
                # the index file is supposed to reference a lot of stuff
                # so I don't want it to pollute the backlinks
                continue

            with open(f'{notes_folder}/{other_file}', 'r') as f:
                contents = f.read()

                # the results of re.findall() will look something like
                # [('Page B', 'pageB.md')]
                # where the link in markdown would've been [Page B](pageB.md)
                for _, link in md_links.findall(contents):
                    if link == file_name:
                        logger.debug(f'{file_name}: referenced by {other_file}')
                        title = util.note_title(f'{notes_folder}/{other_file}')
                        references.append((other_file, title))

        # write out all of the backlinks using some properly styled markdown.
        # this bit will be appended to the original note later on when it is
        # converted to a standalone HTML page
        backlinks_file_path = f'{backlinks_folder}/{file_name}.backlinks'
        with open(backlinks_file_path, 'w') as f:
            f.write(backlinks_html(refs=references))
