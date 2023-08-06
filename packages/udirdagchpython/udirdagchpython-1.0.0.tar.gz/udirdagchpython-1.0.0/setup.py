import setuptools 
from pathlib import Path

setuptools.setup(
    name="udirdagchpython",version="1.0.0",
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=[".vscode", "turshikh.py","tests", "data"])
)