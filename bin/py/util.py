import logging
import pathlib
import subprocess
import sys


def get_logger(logger_name: str) -> logging.Logger:
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(name)s: %(levelname)s - %(message)s'))

    logger = logging.getLogger(name=logger_name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger


def last_n_chars(s: str, n: int) -> str:
    return s[-n::]


def is_md(file_name_with_extension: str) -> bool:
    return last_n_chars(file_name_with_extension, n=3) == '.md'


def first_line(file_path: str) -> str:
    with open(file_path, 'r') as f:
        first_line_in_file = f.readline()
        return first_line_in_file[2:]


def create_folder(location: str) -> None:
    pathlib.Path(location).mkdir(parents=True, exist_ok=True)


def convert_to_html(output_filename: str, *args: str) -> None:
    """
    call pandoc
    """
    print(f'output_filename={output_filename}')
    print(f'*args={args}')
    # examples of using subprocess.run
    # https://www.programcreek.com/python/example/94463/subprocess.run
    # subprocess.run(
    #     [
    #         'pandoc',
    #         path_of_original_file,
    #
    #     ]
    # )
    '''
    pandoc \
        "$@" \
        -f markdown \
        -t html5 \
        -o "$HTML_FOLDER_REL/$(strip_file_ext "$(basename "$FILE")").html" \
        --lua-filter="$DIR/links_to_html.lua" \
        --include-in-header="$DIR/meta/meta.html" \
        --metadata pagetitle="$(first_line "$FILE")" \
        --include-before-body="$DIR/meta/meta-before-body.html" \
        --include-after-body="$DIR/meta/meta-after-body.html"
    '''
    pass
