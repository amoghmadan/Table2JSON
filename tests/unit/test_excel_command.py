import os
import unittest

from table2json.bin import execute_from_command_line
from table2json.core.helpers import call_command
from table2json.utils.getter import get_name
from tests import ASSETS_DIR


class TestExcelCommand(unittest.TestCase):
    """Test Excel Command"""

    command = "excel"

    def test_excel_command(self):
        """Test Excel"""

        options = {
            "path": os.path.abspath(ASSETS_DIR / "input.xlsx"),
            "sheet": "Sheet1",
        }
        argv = [get_name(), self.command, options["path"], "-S", options["sheet"]]
        self.assertEqual(execute_from_command_line(argv), None)

    def test_help_by_command_name(self):
        """Test Help By Command Name"""

        with self.assertRaises(SystemExit):
            call_command(self.command, "--help", verbosity=0)

    def test_version_by_command_name(self):
        """Test Version By Command Name"""

        with self.assertRaises(SystemExit):
            call_command(self.command, "--version", verbosity=0)

    def test_unknown_args(self):
        """Test Unknown Command Error"""

        argv = [get_name(), self.command, "path", "-l", "82"]
        with self.assertRaises(SystemExit):
            execute_from_command_line(argv)
