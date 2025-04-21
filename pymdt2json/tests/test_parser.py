import pytest
import tempfile
import os
from pymdt2json import MinifyMDT

# Import the parser class (already defined)
# from previous cell: MarkdownTable2Json


# Helper to write temporary markdown file
def write_temp_md(content):
    fd, path = tempfile.mkstemp(suffix=".md", text=True)
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(content)
    return path


# Edge Case Markdown Inputs
cases = {
    "standard_table": {
        "table": "| Name | Age |\n|------|-----|\n| Alice | 30 |\n| Bob | 25 |",
        "json": '[{"Name":"Alice","Age":"30"},{"Name":"Bob","Age":"25"}]'
    },
    "table_with_extra_spaces": {
        "table":
            "| Name     |   Age   |\n|----------|--------|\n| Alice    |  30    |\n| Bob      |   25   |",
        "json":
            '[{"Name":"Alice","Age":"30"},{"Name":"Bob","Age":"25"}]'
    },
    "table_with_empty_cells": {
        "table":
            "| Name | Age | City |\n|------|-----|------|\n| Alice | 30 | |\n| Bob | | Berlin |",
        "json":
            '[{"Name":"Alice","Age":"30","City":""},{"Name":"Bob","Age":"","City":"Berlin"}]'
    },
    "table_with_leading_text": {
        "table": "Here is a table:\n\n| A | B |\n|---|---|\n| x | y |\n| z | w |",
        "json": '[{"A":"x","B":"y"},{"A":"z","B":"w"}]'
    },
    "multiple_tables": {
        "table": "| X | Y |\n|---|---|\n| 1 | 2 |\n\n| A | B |\n|---|---|\n| x | y |",
        "json": '[{"X":"1","Y":"2"}]'
    },
}


@pytest.mark.parametrize("case_name,case_data", cases.items())
def test_markdown_table_to_json(case_name: str, case_data: dict):
    markdown, expected_fragment = case_data.values()
    parser = MinifyMDT(markdown_string=markdown, layout="AoS", minify=True)
    result = parser.transform()

    assert "```json" in result
    assert expected_fragment in result


if __name__ == "__main__":
    test_results = {}
    for name, data in cases.items():
        test_markdown_table_to_json(name, data)
