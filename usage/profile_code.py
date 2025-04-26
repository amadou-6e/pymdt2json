import cProfile
import time
from pathlib import Path
from llama_index.core import SimpleDirectoryReader
from pymdt2json.src.parser import MinifyMDT


def main():
    source_dir = Path("usage", "markdown")

    documents = SimpleDirectoryReader(source_dir, required_exts=[".md"], recursive=True).load_data()
    print(f"Loaded {len(documents)} documents")

    for idx, doc in enumerate(documents):
        print(idx)
        start = time.time()
        markdown_text = MinifyMDT(doc.text_resource.text).transform()
        end = time.time()
        print("Took", end - start, "seconds")

        with open(f"output{idx}.md", "w", encoding="utf-8") as f:
            f.write(markdown_text)


if __name__ == "__main__":
    cProfile.run('main()', filename='output.prof')
