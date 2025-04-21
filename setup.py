from setuptools import setup, find_packages

setup(
    name="pymdt2json",
    version="0.1.0",
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
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    include_package_data=True,
)
