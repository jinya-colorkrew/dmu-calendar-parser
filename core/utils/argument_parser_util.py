from typing import Tuple, Optional
from argparse import ArgumentParser


class ArgumentParserUtil:
    def handle() -> Tuple[str, Optional[str]]:
        parser = ArgumentParser()
        parser.add_argument(
            "-s",
            "--source",
            required=True,
            help="source file path.",
        )
        parser.add_argument(
            "-o",
            "--output",
            required=False,
            help="output file path. result csv will be outputted to specified path",
        )
        args = parser.parse_args()

        return args.source, args.output
