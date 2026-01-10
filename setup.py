#!/usr/bin/env python3
from setuptools import setup
from pathlib import Path

readme = Path(__file__).parent / "README.md"
long_description = readme.read_text(encoding='utf-8') if readme.exists() else ""

setup(
    name="dataconvert",
    version="1.0.0",
    description="Universal data format converter - JSON, CSV, XML, YAML - zero dependencies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Holy Grail Automation",
    url="https://github.com/DonkRonk17/DataConvert",
    py_modules=["dataconvert"],
    install_requires=[],
    entry_points={"console_scripts": ["dataconvert=dataconvert:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.6",
    keywords="data-converter json csv xml yaml format-conversion",
)
