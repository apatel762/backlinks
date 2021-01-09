# ---------------------------------------------------------------------------
# IMPORTS

import os
import re
import argparse
import pathlib
from typing import List, Tuple

# ---------------------------------------------------------------------------
# REGEXES

# regular expression for finding markdown style links
# i.e. something like `[My Link](https://broadsilver.com)`
md_links = re.compile("\[(.*?)\]\((.*?)\)", re.DOTALL)

# regular expression for finding roam style links where the content of the
# link is just the name of the file that you're linking to
# i.e. something like `[[My Link]]`
roam_links = re.compile("\[\[(.*?)\]\]", re.DOTALL)


# ---------------------------------------------------------------------------
# BEGIN SCRIPT

def last_n_chars(s: str, n: int) -> str:
    return s[-n::]


def is_md(file_name: str) -> bool:
    return last_n_chars(file_name, n=3) == '.md'


def markdown_filenames(folder_path: str) -> List[str]:
    return [fn for fn in os.listdir(folder_path) if is_md(file_name=fn)]


def html_link(link: str, display: str) -> str:
    # for some reason pandoc doesn't change the .md to .html in backlinks
    # so the replacement here is a little hack to make it work
    return f'<a href="{link.replace(".md", ".html")}">{display}</a>'


def create_folder(location: str) -> None:
    pathlib.Path(location).mkdir(parents=True, exist_ok=True)


def first_line(file_path: str) -> str:
    title = ''
    with open(file_path, 'r') as f:
        first_line = f.readline()
        title = first_line[2:]
    return title


def backlinks_html(refs: List[Tuple[str, str]]) -> str:
    if len(refs) <= 0:
        return ''

    txt: List[str] = []
    txt.append('<div class="footer">')
    txt.append('<h3>Links</h3>')
    txt.append('<ul>')
    for backlink, display in set(refs):
        txt.append('<li>' + html_link(backlink, display) + '</li>')
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

    notes_folder = args.notes_folder
    backlinks_folder = args.temp_folder

    file_names = markdown_filenames(folder_path=notes_folder)
    print(f'Found {len(file_names)} files in {notes_folder}')

    create_folder(location=backlinks_folder)
    print(f'Will put backlinks into: {backlinks_folder}/')

    # NOTE: current backlink searching is slow... O(n^2)
    for file_name in file_names:
        # a list of all of the files that reference this one
        references = []

        # look in all of the other files for references and put them in the
        # above list if we find any
        for other_file in file_names:
            if other_file == file_name:
                continue

            with open(f'{notes_folder}/{other_file}', 'r') as f:
                contents = f.read()

                # the results of re.findall() will look something like
                # [('Page B', 'pageB.md')]
                # where the link in markdown would've been [Page B](pageB.md)
                for display, link in md_links.findall(contents):
                    if link == file_name:
                        print(f'{file_name}: referenced by {other_file}')
                        title = first_line(f'{notes_folder}/{other_file}')
                        references.append((other_file, title))

                # for roam style links the results of re.findall() will just
                # be a list of stuff like:
                # ['pageA']
                # where in markdown the link would've been something like:
                #   blah blah [[pageA]]
                for display in roam_links.findall(contents):
                    if display == file_name[:-len('.md')]:
                        print(f'{file_name}: [[referenced]] by {other_file}')
                        title = first_line(f'{notes_folder}/{other_file}')
                        references.append((other_file, title))

        # write out all of the backlinks using some properly styled markdown.
        # this bit will be appended to the original note later on when it is
        # converted to a standalone HTML page
        backlinks_file_path = f'{backlinks_folder}/{file_name}.backlinks'
        with open(backlinks_file_path, 'w') as f:
            f.write(backlinks_html(refs=references))
