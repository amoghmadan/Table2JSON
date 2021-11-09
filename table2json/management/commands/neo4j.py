import sys
from getpass import getpass

try:
    import neo4j
except ModuleNotFoundError:
    msg = "Install optional dependency neo4j, pip install table2json[neo4j]"
    sys.exit(msg)
from pandas import DataFrame

from table2json.extended.base import Table2JSONBaseCommand


class Command(Table2JSONBaseCommand):
    """Neo4j Command"""

    help = "Read from Neo4j Tabular Query write to JSON"

    def add_command_arguments(self, parser):
        """Add Arguments for Neo4j Command"""

        parser.add_argument("user", type=str, help="Neo4j user to connect")
        parser.add_argument(
            "query", type=str, help="Provide query to return tabular data"
        )
        parser.add_argument(
            "-H",
            "--host",
            type=str,
            default="127.0.0.1",
            help="Neo4j host to connect, default=127.0.0.1",
        )
        parser.add_argument(
            "-P",
            "--port",
            type=int,
            default=7687,
            help="Neo4j bolt port to connect, default=7687",
        )
        parser.add_argument(
            "-p", "--password", type=str, help="Neo4j password to connect"
        )

    def process_to_df(self, *args, **options):
        """Neo4j Handling Logic"""

        if not options["password"]:
            options["password"] = getpass(prompt="Password: ", stream=None)
        uri = "bolt://%s:%d" % (options["host"], options["port"])
        auth = (options["user"], options["password"])
        with neo4j.GraphDatabase.bolt_driver(uri, auth=auth) as driver:
            with driver.session() as session:
                records = session.run(options["query"])
        return DataFrame([r.values() for r in records], columns=records.keys())
