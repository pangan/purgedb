import sys
import json
from mysql import connector

def _get_config(filepath: str) -> dict:
    with open(filepath) as config_file:
        return json.load(config_file)


def _get_mysql_connection(connection, database):
    return connector.connect(
        host=connection['host'],
        user=connection['user'],
        password=connection['password'],
        database=database
    )
def _do_purge(config):
    for database, tables in config['databases'].items():
        mydb = _get_mysql_connection(config['connection'], database)
        mycursor = mydb.cursor()

        for table, query in tables.items():
            sql = f"DELETE FROM {table} WHERE {query}"
            mycursor.execute(sql)
            mydb.commit()

def run_app():
    if len(sys.argv) == 1:
        print('Error: config file is missed!')
        exit(1)

    config = _get_config(sys.argv[1])

    _do_purge(config)

    return True

