import logging
import os
import pathlib
import subprocess
import sys
from typing import List


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
        return f.readline()


def note_title(file_path: str) -> str:
    return first_line(file_path) \
        .replace('# ', '') \
        .replace('\n', '')


def change_file_extension(file_path: str, new_ext: str) -> str:
    fp: pathlib.Path = pathlib.Path(file_path)
    fp: pathlib.Path = fp.with_suffix('')
    fp: pathlib.Path = fp.with_suffix(new_ext)
    return str(fp)


def create_folder(location: str) -> None:
    pathlib.Path(location).mkdir(parents=True, exist_ok=True)


def path(*args: str) -> str:
    return os.sep.join(args)


def run(cmd: List[str]) -> None:
    """
    you don't have to quote args that have spaces when you aren't using them
    in a shell; Python handles this for you.

    examples of using subprocess.run
        https://www.programcreek.com/python/example/94463/subprocess.run
    """
    subprocess.run(
        args=cmd,
        env={
            'PATH': os.environ['PATH']
        },
        check=True,
        text=True
    )
