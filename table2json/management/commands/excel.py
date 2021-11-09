import sys

from pandas import read_excel

from table2json.extended.base import Table2JSONBaseCommand


class Command(Table2JSONBaseCommand):
    """Excel Command"""

    help = "Read from Excel Sheet write to JSON"

    def add_command_arguments(self, parser):
        """Add Arguments for Excel Command"""

        parser.add_argument("path", type=str, help="Path to the Excel file")
        parser.add_argument(
            "-S",
            "--sheet",
            type=str,
            default="Sheet1",
            help="Provide name of sheet, default=Sheet1",
        )

    def process_to_df(self, *args, **options):
        """Excel Handling Logic"""

        try:
            return read_excel(options["path"], sheet_name=options["sheet"])
        except ImportError:
            msg = "Install optional dependency excel, pip install table2json[excel]"
            sys.exit(msg)
