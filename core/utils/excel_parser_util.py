import pyexcel
from typing import Dict, List, Tuple


class ExcelParserUtil:
    def parse_book(book_name: str) -> Dict:
        return pyexcel.get_book_dict(file_name=book_name)

    def parse_sheet(content_matrix: List[List]) -> Tuple[List, List]:
        header = content_matrix[1]
        body = content_matrix[2:]

        return header, body
