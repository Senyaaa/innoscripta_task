from typing import List
from html_table_parser import HTMLTableParser
import re


def get_raw_html(path_to_html_file: str) -> str:
    with open(path_to_html_file, encoding='utf-8') as html_file:
        return html_file.read()


def parse_for_tables(path_to_html_file: str) -> List[List[str]]:
    raw_html = get_raw_html(path_to_html_file)

    html_parser_instance = HTMLTableParser(
        decode_html_entities=True,
        data_separator=' '
    )

    html_parser_instance.feed(raw_html)
    return html_parser_instance.tables


def flat(data: List[List[str]]) -> List[str]:
    flat_list_without_blanks = [
        item for item in [
            item for sublist in [
                [item] if not isinstance(item, list) else item for item in data
            ] for item in sublist
        ] if item != '']
    return flat_list_without_blanks


def concat(data: List[str], sep=' ') -> str:
    return sep.join(data)


def preprocess(data: List[List[str]], remove_level_system: bool = False) -> str:
    data = concat(flat(data))
    data = re.sub("-", " ", data)  # Removing -
    data = re.sub("\s\s+", " ", data)  # Removing multiple spaces
    if remove_level_system:
        # Working on the level system
        data = re.sub("\s[IVX]+.\s", " ", data)  # Removing I/II/III/IV
        data = re.sub("\s[1-9]+.\s", " ", data)  # Removing 1/2/3/4
        data = re.sub("\s[A-Z].\s", " ", data)  # Removing A/B/C/D
        data = re.sub("\s[+&]\s", " ", data)  # Removing +/&
        data = re.sub(",\s", " ", data)  # Removing ,
    return data