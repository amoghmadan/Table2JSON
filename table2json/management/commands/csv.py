from pandas import read_csv

from table2json.management import Table2JSONBaseCommand


class Command(Table2JSONBaseCommand):
    """CSV Command"""

    help = "Read from XSV write to JSON"

    def add_command_arguments(self, parser):
        """Add Arguments for CSV Command"""

        parser.add_argument("path", type=str, help="Path to the XSV file")

    def process_to_df(self, *args, **options):
        """CSV Handling Logic"""

        return read_csv(options["path"])
