from .src.parser import MinifyMDT
from .src.cli import create_parser

__all__ = ["MinfyMDT"]


def main():
    create_parser()
