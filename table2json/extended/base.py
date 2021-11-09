from __future__ import annotations

import json
from datetime import datetime

from table2json.core.base import BaseCommand
from table2json.utils.getter import get_version


class Table2JSONBaseCommand(BaseCommand):
    """Optional Arguments Base Command"""

    version = get_version()

    def add_command_arguments(self, parser):
        """Add Command Specific Arguments"""

        raise NotImplementedError(
            "subclasses of %s must provide a add_command_arguments() method"
            % (self.__class__.__name__,)
        )

    def add_arguments(self, parser):
        """Add Optional Arguments for all the Commands"""

        now = datetime.now().strftime("%Y-%m-%dT%H-%M-%S.%fZ")

        self.add_command_arguments(parser)
        parser.add_argument(
            "-o",
            "--outfile",
            type=str,
            default="output-[%s].json" % (now,),
            help="Provide path to output JSON file, default=output-[datetime].json",
        )
        parser.add_argument(
            "-e",
            "--encoding",
            type=str,
            default="utf-8",
            help="Provide encoding for output JSON file, default=utf-8",
        )
        parser.add_argument(
            "-i",
            "--indent",
            type=int,
            default=4,
            help="Provide indent for output JSON file, default=4",
        )

    def process_to_df(self, *args, **options):
        """Process to DataFrame"""

        raise NotImplementedError(
            "subclasses of %s must provide a process_to_df() method"
            % (self.__class__.__name__,)
        )

    @staticmethod
    def process_outfile(df, **options):
        """Create JSON File from DataFrame"""

        records = df.to_json(orient="records")
        with open(options["outfile"], mode="w", encoding=options["encoding"]) as fp:
            json.dump(
                json.loads(records),
                fp,
                ensure_ascii=False,
                indent=options["indent"],
                default=str,
            )

    def handle(self, *args, **options):
        """The actual logic of the command."""

        df = self.process_to_df(*args, **options)
        self.process_outfile(df, **options)
