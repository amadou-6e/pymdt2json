import json
import markdown
import html2text
from bs4 import BeautifulSoup


class MinifyMDT:

    def __init__(self, markdown_text, layout="SoA", minify=True):
        self.markdown_text = markdown_text
        self.layout = layout
        self.minify = minify
        self._json_kwargs = {
            "separators": (",", ":"),
            "indent": None
        } if self.minify else {
            "indent": 2
        }

    def _html_table_to_markdown(self, table_tag):
        """
        Converts a BeautifulSoup <table> tag to clean Markdown table text.
        """
        rows = []
        for tr in table_tag.find_all("tr"):
            cells = tr.find_all(["td", "th"])
            row = "| " + " | ".join(cell.get_text(strip=True) for cell in cells) + " |"
            rows.append(row)

        if len(rows) >= 2:
            # Insert a separator after header
            num_cols = rows[0].count("|") - 1
            separator = "| " + " | ".join(["---"] * num_cols) + " |"
            rows.insert(1, separator)

        return "\n".join(rows)

    def _table_to_json(self, header, rows):
        if self.layout == "AoS":
            return [{
                header[i]: row[i] for i in range(min(len(header), len(row)))
            } for row in rows if len(row) == len(header)]
        else:  # SoA
            table = {col: [] for col in header}
            for row in rows:
                for i, col in enumerate(header):
                    table[col].append(row[i] if i < len(row) else None)
            return table

    def transform(self):
        # 1) Markdown → HTML
        html = markdown.markdown(self.markdown_text, extensions=["tables"])

        # 2) Parse HTML
        soup = BeautifulSoup(html, "html.parser")

        # 3) Find all tables
        for table in soup.find_all("table"):
            table_md = self._html_table_to_markdown(table)

            lines = [line.strip() for line in table_md.splitlines()]
            if len(lines) < 2:
                continue  # skip malformed tables

            header = lines[0].strip("|").split("|")
            rows = [line.strip("|").split("|") for line in lines[2:] if line.strip()]
            json_obj = self._table_to_json(header, rows)
            json_str = json.dumps(json_obj, **self._json_kwargs)

            # Create a <pre> tag with the JSON code block
            pre_tag = soup.new_tag("pre")
            pre_tag.string = f"```json\n{json_str}\n```"
            table.replace_with(pre_tag)

        # 4) HTML → Markdown
        clean_html = str(soup)
        final_markdown = html2text.HTML2Text().handle(clean_html)

        return final_markdown


if __name__ == "__main__":
    from pathlib import Path

    md_sample_path = Path("usage",
                          "markdown")  # Path("pymdt2json", "tests", "assets", "small_sample.md")
    assert md_sample_path.exists()

    with md_sample_path.open("r", encoding="utf-8") as file:
        md_text = file.read()

    parser = MinifyMDT(markdown_text=md_text, layout="AoS", minify=True)
    result = parser.transform()
    print(result)
