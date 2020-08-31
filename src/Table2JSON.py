import sys
import json
import argparse
from getpass import getpass
from datetime import datetime

import sqlite3
import pandas as pd
from MySQLdb import Connection
from neo4j import GraphDatabase, Result


class Table2JSON(object):
    """."""

    index = False

    def __init__(self):
        """."""

        out_file = 'output_{}.json'.format(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

        parser = argparse.ArgumentParser(description='')
        sub_parser = parser.add_subparsers(title='commands', dest='command')

        csv = sub_parser.add_parser('csv', help='Read from XSV write to JSON')
        csv.add_argument('path', type=str, help='Provide path of JSON file')
        csv.add_argument('-o', '--outfile', type=str, default=out_file,
                         help='Provide path to output JSON file, default=output_datetime.json')

        excel = sub_parser.add_parser('excel', help='Read from Excel Sheet write to JSON')
        excel.add_argument('path', type=str, help='Provide path of Excel file')
        excel.add_argument('-S', '--sheet', type=str, default='Sheet1', help='Provide name of sheet, default=Sheet1')
        excel.add_argument('-o', '--outfile', type=str, default=out_file,
                           help='Provide path to output JSON file, default=output_datetime.json')

        sqlite = sub_parser.add_parser('sqlite', help='Read from SQLite query write to JSON')
        sqlite.add_argument('path', type=str, help='Provide path of SQLite file')
        sqlite.add_argument('query', type=str, help='Provide query to return tabular data')
        sqlite.add_argument('-o', '--outfile', type=str, default=out_file,
                            help='Provide path to output JSON file, default=output_datetime.json')

        mysql = sub_parser.add_parser('mysql', help='Read from MySQL query write to JSON')
        mysql.add_argument('user', type=str, help='MySQL user to connect')
        mysql.add_argument('database', type=str, help='MySQL db to connect')
        mysql.add_argument('query', type=str, help='Provide query to return tabular data')
        mysql.add_argument('-H', '--host', type=str, default='127.0.0.1',
                           help='MySQL host to connect, default=127.0.0.1')
        mysql.add_argument('-p', '--port', type=int, default=3306, help='MySQL port to connect, default=3306')
        mysql.add_argument('-o', '--outfile', type=str, default=out_file,
                           help='Provide path to output JSON file, default=output_datetime.json')

        neo4j = sub_parser.add_parser('neo4j', help='Read from Neo4j query write to JSON')
        neo4j.add_argument('user', type=str, help='Neo4j user to connect')
        neo4j.add_argument('query', type=str, help='Provide query to return tabular data')
        neo4j.add_argument('-H', '--host', type=str, default='127.0.0.1',
                           help='Neo4j host to connect, default=127.0.0.1')
        neo4j.add_argument('-p', '--port', type=int, default=7687, help='Neo4j port to connect, default=7687')
        neo4j.add_argument('-o', '--outfile', type=str, default=out_file,
                           help='Provide path to output JSON file, default=output_datetime.json')

        self.args = parser.parse_args()

    @staticmethod
    def csv2json(**kwargs: dict) -> pd.DataFrame:
        """."""

        return pd.read_csv(kwargs['path'])

    @staticmethod
    def excel2json(**kwargs: dict) -> pd.DataFrame:
        """."""

        return pd.read_excel(kwargs['path'], sheet_name=kwargs['sheet'])

    @staticmethod
    def sqlite2json(**kwargs: dict) -> pd.DataFrame:
        """."""

        with sqlite3.connect(kwargs['path']) as connection:
            df: pd.DataFrame = pd.read_sql_query(kwargs['query'], con=connection)
        return df

    @staticmethod
    def mysql2json(**kwargs: dict) -> pd.DataFrame:
        """."""

        password: str = getpass(prompt='Password: ', stream=None)
        with Connection(host=kwargs['host'], port=kwargs['port'], user=kwargs['user'], passwd=password, db=kwargs['database']) as connection:
            df: pd.DataFrame = pd.read_sql(kwargs['query'], con=connection)
        return df

    @staticmethod
    def neo4j2json(**kwargs: dict) -> pd.DataFrame:
        """."""

        password: str = getpass(prompt='Password: ', stream=None)
        uri: str = 'bolt://{}:{}'.format(kwargs['host'], kwargs['port'])
        driver: GraphDatabase = GraphDatabase.driver(uri, auth=(kwargs['user'], password))
        with driver.session() as session:
            records: Result = session.run(kwargs['query'])
        driver.close()
        return pd.DataFrame([record.values() for record in records], columns=records.keys())

    def run(self) -> None:
        """."""

        call: dict = {
            'csv': self.csv2json,
            'excel': self.excel2json,
            'sqlite': self.sqlite2json,
            'mysql': self.mysql2json,
            'neo4j': self.neo4j2json,
        }

        if self.args.command not in call:
            sys.exit('Please enter a sub command, for help use -h flag')

        df: pd.DataFrame = call[self.args.command](**vars(self.args))
        json_data: list = json.loads(df.to_json(orient='records'))

        with open(self.args.outfile, 'w') as fp:
            json.dump(json_data, fp, indent=4, default=str)


if __name__ == '__main__':
    """."""

    try:
        table2json: Table2JSON = Table2JSON()
        table2json.run()

    except Exception as exc:
        tc, te, tb = sys.exc_info()
        print('{}: {}'.format(tc.__name__, exc))
