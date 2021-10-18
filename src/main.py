from __future__ import annotations

import json
import sqlite3
import sys
from argparse import ArgumentParser, Namespace
from datetime import datetime
from getpass import getpass

from MySQLdb import Connection
from neo4j import GraphDatabase, Result
from pandas import read_csv, read_excel, read_sql, read_sql_query, DataFrame

__version__ = "1.0.0"


class Table2JSON(object):
    """Table2JSON"""

    now: str = datetime.now().strftime("%Y-%m-%dT%H-%M-%S.%fZ")
    extra_optional_arguments: list = [
        {
            "short": "-o",
            "long": "--outfile",
            "type": str,
            "default": "output-[%s].json" % (now,),
            "help": "Provide path to output JSON file, default=output-[datetime].json",
        },
        {
            "short": "-e",
            "long": "--encoding",
            "type": str,
            "default": "utf-8",
            "help": "Provide encoding for output JSON file, default=utf-8",
        },
        {
            "short": "-i",
            "long": "--indentation",
            "type": int,
            "default": 4,
            "help": "Provide indentation, default=4",
        },
    ]

    def __init__(self: Table2JSON) -> None:
        """Setup Parser and Sub-parsers"""

        # Version Display
        version: str = "%s %s" % (self.__class__.__name__, __version__)

        # Parser / Sub Parser
        parser: ArgumentParser = ArgumentParser(description="Table2JSON")
        parser.add_argument("-v", "--version", action="version", version=version)
        sub_parser = parser.add_subparsers(title="commands", dest="command")

        # Declare Sub Commands
        csv: ArgumentParser = sub_parser.add_parser(
            "csv", help="Read from XSV write to JSON"
        )
        csv.add_argument("path", type=str, help="Provide path of XSV file")

        excel: ArgumentParser = sub_parser.add_parser(
            "excel", help="Read from Excel Sheet write to JSON"
        )
        excel.add_argument("path", type=str, help="Provide path of Excel file")
        excel.add_argument(
            "-S",
            "--sheet",
            type=str,
            default="Sheet1",
            help="Provide name of sheet, default=Sheet1",
        )

        sqlite: ArgumentParser = sub_parser.add_parser(
            "sqlite", help="Read from SQLite query write to JSON"
        )
        sqlite.add_argument("path", type=str, help="Provide path of SQLite file")
        sqlite.add_argument(
            "query", type=str, help="Provide query to return tabular data"
        )

        mysql: ArgumentParser = sub_parser.add_parser(
            "mysql", help="Read from MySQL query write to JSON"
        )
        mysql.add_argument("user", type=str, help="MySQL user to connect")
        mysql.add_argument("database", type=str, help="MySQL db to connect")
        mysql.add_argument(
            "query", type=str, help="Provide query to return tabular data"
        )
        mysql.add_argument(
            "-H",
            "--host",
            type=str,
            default="127.0.0.1",
            help="MySQL host to connect, default=127.0.0.1",
        )
        mysql.add_argument(
            "-p",
            "--port",
            type=int,
            default=3306,
            help="MySQL port to connect, default=3306",
        )

        neo4j: ArgumentParser = sub_parser.add_parser(
            "neo4j", help="Read from Neo4j query write to JSON"
        )
        neo4j.add_argument("user", type=str, help="Neo4j user to connect")
        neo4j.add_argument(
            "query", type=str, help="Provide query to return tabular data"
        )
        neo4j.add_argument(
            "-H",
            "--host",
            type=str,
            default="127.0.0.1",
            help="Neo4j host to connect, default=127.0.0.1",
        )
        neo4j.add_argument(
            "-p",
            "--port",
            type=int,
            default=7687,
            help="Neo4j bolt port to connect, default=7687",
        )

        # Add Extra Optional Arguments
        commands: list = [choice for choice in sub_parser.choices.values()]
        for command in commands:
            for entry in self.extra_optional_arguments:
                command.add_argument(
                    entry["short"],
                    entry["long"],
                    type=entry["type"],
                    default=entry["default"],
                    help=entry["help"],
                )

        # Get Arguments Passed By User
        self.args: Namespace = parser.parse_args()

    @staticmethod
    def csv2df(**kwargs: str) -> DataFrame:
        """Process CSV"""

        return read_csv(kwargs["path"])

    @staticmethod
    def excel2df(**kwargs: str) -> DataFrame:
        """Process Excel"""

        return read_excel(kwargs["path"], sheet_name=kwargs["sheet"])

    @staticmethod
    def sqlite2df(**kwargs: str) -> DataFrame:
        """Process SQLite"""

        with sqlite3.connect(kwargs["path"]) as connection:
            df: DataFrame = read_sql_query(kwargs["query"], con=connection)
        return df

    @staticmethod
    def mysql2df(**kwargs: str | int) -> DataFrame:
        """Process MySQL"""

        kwargs["passwd"] = getpass(prompt="Password: ", stream=None)
        with Connection(**kwargs) as connection:
            df: DataFrame = read_sql(kwargs["query"], con=connection)
        return df

    @staticmethod
    def neo4j2df(**kwargs: str | int) -> DataFrame:
        """Process Neo4j"""

        password: str = getpass(prompt="Password: ", stream=None)
        uri: str = "bolt://%s:%d" % (kwargs["host"], kwargs["port"])
        auth: tuple = (kwargs["user"], password)
        with GraphDatabase.bolt_driver(uri, auth=auth) as driver:
            with driver.session() as session:
                records: Result = session.run(kwargs["query"])
        return DataFrame([r.values() for r in records], columns=records.keys())

    def process(self: Table2JSON) -> None:
        """Process"""

        if not self.args.command:
            sys.exit("Please enter a sub command, for help use -h flag")

        function_name: str = self.args.command + "2df"
        if not hasattr(self, function_name):
            sys.exit(
                "Process for sub command %r is not implemented" % (self.args.command,)
            )

        df: DataFrame = getattr(self, function_name)(**vars(self.args))
        records: list = json.loads(df.to_json(orient="records"))
        with open(self.args.outfile, "w", encoding=self.args.encoding) as fp:
            json.dump(records, fp, indent=self.args.indentation, default=str)


def main():
    """Main"""

    try:
        table2json: Table2JSON = Table2JSON()
        table2json.process()
    except Exception as exc:
        tc, te, tb = sys.exc_info()
        sys.stdout.write("%s: %s" % (tc.__name__, exc))


if __name__ == "__main__":
    """Scope"""

    main()
