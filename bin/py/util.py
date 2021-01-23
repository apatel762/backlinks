import logging
import pathlib
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
