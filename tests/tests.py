import os
import sys
import unittest
from pathlib import Path

from pandas import DataFrame

BASE_DIR = Path(__file__).parent.parent
sys.path.append(os.path.abspath(BASE_DIR))


class TestTable2JSON(unittest.TestCase):
    """Test Table2JSON"""

    ASSETS_DIR = BASE_DIR / "assets"

    def test_csv2df(self):
        """Test CSV"""

        from table2json.management.commands.csv import Command

        kwargs = {"path": self.ASSETS_DIR / "input.csv"}
        command = Command()
        result = command.process_to_df(**kwargs)
        self.assertTrue(isinstance(result, DataFrame))

    def test_excel2df(self):
        """Test Excel"""

        from table2json.management.commands.excel import Command

        kwargs = {"path": self.ASSETS_DIR / "input.xlsx", "sheet": "Sheet1"}
        command = Command()
        result = command.process_to_df(**kwargs)
        self.assertTrue(isinstance(result, DataFrame))

    @unittest.skip("MySQL, Switch Test Credentials")
    def test_mysql2df(self):
        """Test MySQL"""

        from table2json.management.commands.mysql import Command

        kwargs = {"user": "root", "password": "root", "query": "SELECT 1 AS One;"}
        command = Command()
        result = command.process_to_df(**kwargs)
        self.assertTrue(isinstance(result, DataFrame))

    @unittest.skip("Neo4j, Switch Test Credentials")
    def test_neo4j2df(self):
        """Test Neo4j"""

        from table2json.management.commands.neo4j import Command

        kwargs = {"user": "neo4j", "password": "neo4j", "query": "MATCH 1 AS One;"}
        command = Command()
        result = command.process_to_df(**kwargs)
        self.assertTrue(isinstance(result, DataFrame))

    def test_sqlite2df(self):
        """Test SQLite"""

        from table2json.management.commands.sqlite import Command

        kwargs: dict = {
            "path": self.ASSETS_DIR / "input.sqlite3",
            "query": "SELECT id FROM One;",
        }
        command = Command()
        result = command.process_to_df(**kwargs)
        self.assertTrue(isinstance(result, DataFrame))