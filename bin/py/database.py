import sqlite3
from datetime import datetime

import util


class DatabaseConnector(object):
    def __init__(self, db_file: str):
        self.db_file = db_file

    def __enter__(self) -> sqlite3.Connection:
        self.conn: sqlite3.Connection = sqlite3.connect(self.db_file)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


table_runs_name = 'script_runs'


def create_script_runs_table(connection: sqlite3.Connection) -> None:
    create_table: str = f'''
    CREATE TABLE IF NOT EXISTS {table_runs_name}
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_of_run TEXT UNIQUE
    )
    '''
    connection.execute(create_table)
    connection.commit()


def record_script_runtime(connection: sqlite3.Connection) -> None:
    insert: str = f'''
    INSERT OR IGNORE INTO {table_runs_name} (date_of_run)
    VALUES (?)
    '''
    connection.execute(insert, (util.now_utc(),))
    connection.commit()


def get_latest_script_runtime(connection: sqlite3.Connection) -> datetime:
    select: str = f'''
    SELECT date_of_run
    FROM {table_runs_name}
    ORDER BY date_of_run DESC
    '''
    d: str = connection.execute(select).fetchone()
    return datetime.strptime(d[0], util.datetime_format)


if __name__ == '__main__':
    with DatabaseConnector('test.db') as c:
        # TODO: remove after testing
        c.execute('DROP TABLE script_runs')

        create_script_runs_table(connection=c)
        record_script_runtime(connection=c)
        dttm: datetime = get_latest_script_runtime(connection=c)
        print(f'latest runtime of script was {dttm}')
