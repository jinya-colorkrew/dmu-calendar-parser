import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


import re
import pprint
from core import constants
from core.utils.argument_parser_util import ArgumentParserUtil
from core.utils.excel_parser_util import ExcelParserUtil
from sheet_parser import SheetParser
from db_transactor import DbTransactor
from csv_writer import CsvWriter


def main():
    source_path, output_path = ArgumentParserUtil.handle()

    book_dict = ExcelParserUtil.parse_book(source_path)
    for sheet_name, content in book_dict.items():
        if re.match(constants.PARSE_TARGET_SHEET_REGEX, sheet_name):
            # parse sheet and create map
            date_slot_map = SheetParser().handle(sheet_name, content)
            # for d, slots in date_slot_map.items():
            #     print(d)
            #     for slot, subjects in slots.items():
            #         for subject, mapped_slot in subjects.items():
            #             print(f"\t{slot}: {subject}")
            #             print(f"\t\t{mapped_slot}")
            # break

            # insert records into Calendar table
            DbTransactor().handle()

            # output csv file to specified path if neccessary
            if output_path is not None:
                CsvWriter().handle(output_path, sheet_name, date_slot_map)


if __name__ == "__main__":
    main()
