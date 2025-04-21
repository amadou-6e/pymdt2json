from .src.parser import MinifyMDT
from .src.cli import create_parser

__all__ = ["MinfyMDT"]

if __name__ == "__main__":
    create_parser()
