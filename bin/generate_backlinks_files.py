# ---------------------------------------------------------------------------
# IMPORTS

import os
import re
from typing import List

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


def is_markdown_file(file_name: str) -> bool:
    return last_n_chars(file_name, n=3) == '.md'


def markdown_filenames_in_current_directory() -> List[str]:
    return [fn for fn in os.listdir() if is_markdown_file(file_name=fn)]


def markdown_link(display: str, link: str) -> str:
    return f'[{display}]({link})'


if __name__ == '__main__':
    file_names = markdown_filenames_in_current_directory()
    print(f'Found {len(file_names)} files in the current folder')

    # NOTE: current backlink searching is slow... O(n^2)
    for file_name in file_names:
        # a list of all of the files that reference this one
        references = []

        # look in all of the other files for references and put them in the
        # above list if we find any
        for other_file in file_names:
            if other_file == file_name:
                continue

            with open(other_file, 'r') as f:
                contents = f.read()

                # the results of re.findall() will look something like
                # [('Page B', 'pageB.md')]
                # where the link in markdown would've been [Page B](pageB.md)
                for display, link in md_links.findall(contents):
                    if link == file_name:
                        print(f'{file_name}: referenced by {other_file}')
                        references.append(other_file)

                # for roam style links the results of re.findall() will just
                # be a list of stuff like:
                # ['pageA']
                # where in markdown the link would've been something like:
                #   blah blah [[pageA]]
                for display in roam_links.findall(contents):
                    if display == file_name[:-len('.md')]:
                        print(f'{file_name}: [[referenced]] by {other_file}')
                        references.append(other_file)

        # write out all of the backlinks using some properly styled markdown
        # this bit will be appended to the original file later on when the
        # original file is converted to HTML
        with open(file_name + '.backlinks', 'w') as f:
            f.write('\n')
            f.write('---')
            f.write('\n')
            f.write('Backlinks:')
            f.write('\n')
            f.write('\n')
            for backlink in set(references):
                f.write(f'- {markdown_link(display=backlink[:-3], link=backlink)} \n')
