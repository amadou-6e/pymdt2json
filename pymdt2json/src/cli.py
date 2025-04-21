import argparse
import os
from pathlib import Path
import sys

from .parser import MinifyMDT  # assuming your class is saved as `minify_mdt.py`


def transpile_file(in_path: Path, out_path: Path, layout: str, minify: bool):
    with in_path.open("r", encoding="utf-8") as f:
        md = f.read()
    parser = MinifyMDT(markdown_string=md, layout=layout, minify=minify)
    result = parser.transform()
    with out_path.open("w", encoding="utf-8") as f:
        f.write(result)


def create_parser():
    parser = argparse.ArgumentParser(description="Transpile Markdown tables to JSON code blocks.")
    parser.add_argument("-f", "--file", help="Single markdown file to transpile")
    parser.add_argument("-k", "--out-file", help="Output file for the transpiled JSON")
    parser.add_argument("-d", "--dir", help="Directory of markdown files to transpile")
    parser.add_argument("-o", "--out", help="Output directory for the transpiled JSON files")
    parser.add_argument("-l",
                        "--layout",
                        choices=["SoA", "AoS"],
                        default="SoA",
                        help="Layout of JSON output")
    parser.add_argument("-m", "--minify", action="store_true", help="Minify JSON output")

    args = parser.parse_args()

    # Validation
    if not args.file and not args.dir:
        print("[-] No file or directory provided")
        sys.exit(1)
    if not args.out_file and not args.out:
        print("[-] No output file or output directory provided")
        sys.exit(1)
    if args.file and args.dir:
        print("[-] Cannot provide both a file and a directory")
        sys.exit(1)
    if args.out_file and args.out:
        print("[-] Cannot provide both an output file and output directory")
        sys.exit(1)

    print(f"[+] Transpiling using layout: {args.layout}")

    if args.file:
        in_path = Path(args.file)
        out_path = Path(args.out_file)
        transpile_file(in_path, out_path, layout=args.layout, minify=args.minify)

    elif args.dir:
        in_dir = Path(args.dir)
        out_dir = Path(args.out)
        out_dir.mkdir(parents=True, exist_ok=True)
        for file_path in in_dir.glob("*.md"):
            out_path = out_dir / f"json_{file_path.name}"
            transpile_file(file_path, out_path, layout=args.layout, minify=args.minify)
