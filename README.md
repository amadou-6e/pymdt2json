# pymdt2json

**pymdt2json** is the Python version of [`mdtable2json`](https://github.com/amadou-6e/mdtable2json), a TypeScript library and CLI tool that converts markdown tables into structured JSON. This Python version provides equivalent functionality, making it easy to use markdown data in data science workflows, backend services, or preprocessing pipelines for LLM applications.

## Features

- Convert markdown tables to JSON
- CLI tool for batch or single-file processing
- Choose between:
  - **SoA** (Structure of Arrays): `{ "col1": [...], "col2": [...] }`
  - **AoS** (Array of Structures): `[ {col1: ..., col2: ...}, ... ]`
- Optionally minify output JSON

---

## Installation (CLI)

```bash
pip install pymdt2json
```

---

## CLI Usage

```bash
pymdt2json --help
```

### Options

| Option                    | Description                                   |
|---------------------------|-----------------------------------------------|
| `-f, --file <file>`       | Markdown file to transpile                    |
| `-k, --out-file <out>`    | Output file path                              |
| `-d, --dir <dir>`         | Directory containing markdown files           |
| `-o, --out <out>`         | Output directory for transpiled files         |
| `-l, --layout <layout>`   | Layout of JSON output (`SoA` or `AoS`)        |
| `-m, --minify`            | Minify JSON output                            |

---

## Library Usage (Python)

### Installation

```bash
pip install pymdt2json
```

### Example

```python
from pymdt2json import MinifyMDT

markdown_string = '''
| name  | age |
|-------|-----|
| Alice | 30  |
| Bob   | 25  |
'''

parser = MinifyMDT(markdown_string, layout="AoS", minify=True)
print(parser.transform())
```

---

## Use Cases

- Converting markdown tables to structured JSON for web or API use
- Preprocessing markdown data for **LLM pipelines** or **RAG systems**
- Data cleaning, transformation, or downstream analytics workflows

---

## Library Internals

This library uses regular expressions to match and parse markdown tables, then transforms them into JSON strings using the selected layout and formatting options.

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

---

## License

This project is licensed under the [MIT License](LICENSE).
