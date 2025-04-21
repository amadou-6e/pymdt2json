import json
import re


class MinifyMDT:

    def __init__(self, markdown_string, layout="SoA", minify=True):
        self.markdown_string = markdown_string
        self.layout = layout
        self.minify = minify

    def _table_to_json(self, header, rows):
        if self.layout == "AoS":
            return [{header[i]: row[i] for i in range(len(header))} for row in rows]
        else:  # SoA
            return {col: [row[i] for row in rows] for i, col in enumerate(header)}

    def transform(self):
        table_pattern = re.compile(
            r"((?:\|[^\n]*\|[^\n]*\n)+\|[ \t]*[-:]+[^\n]*\n((?:\|[^\n]*\|[^\n]*\n?)+))",
            re.MULTILINE)

        def table_replacer(match):
            table_text = match.group(0).strip()
            lines = [line.strip() for line in table_text.splitlines()]
            header = [cell.strip() for cell in lines[0].strip("|").split("|")]
            rows = [
                [cell.strip() for cell in line.strip("|").split("|")] for line in lines[2:] if line
            ]
            json_obj = self._table_to_json(header, rows)
            json_str = json.dumps(json_obj,
                                  separators=(",", ":") if self.minify else None,
                                  indent=None if self.minify else 2)
            return f"```json\n{json_str}\n```"

        return table_pattern.sub(table_replacer, self.markdown_string)


if __name__ == "__main__":
    from pathlib import Path
    md_sample_path = Path("pymdt2json", "tests", "assets", "small_sample.md")
    assert md_sample_path.exists()
    with md_sample_path.open("r") as file:
        md_text = file.read()
    parser = MarkdownTable2Json(markdown_string=md_text, layout="AoS", minify=True)
    result = parser.transform()
    print(result)
