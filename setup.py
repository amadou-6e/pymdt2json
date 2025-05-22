from pathlib import Path
from setuptools import setup, find_packages


def parse_requirements(filename):
    print(filename)
    return [line for line in Path(filename).read_text().splitlines() if line]


setup(
    name="pymdt2json",
    version="0.4.0",
    description="Convert markdown tables into JSON code blocks",
    author="Amadou Wolfgang Cisse",
    author_email="amadou.6e@googlemail.com",
    url="https://github.com/amadou-6e/pymdt2json.git",  # change this
    packages=find_packages(),  # looks in current dir
    entry_points={
        "console_scripts": ["pymdt2json=pymdt2json:main",],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=parse_requirements("requirements.txt"),
    python_requires=">=3.7",
    include_package_data=True,
)
