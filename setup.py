from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="volstats",
    version="0.1.1",
    description="OHLC-based volatility estimators for financial time series",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Ryan Gorman",
    python_requires=">=3.8",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=[
        "numpy>=1.20",
        "pandas>=1.2"
    ],
    extras_require={
        "test": ["pytest>=6.0"]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    include_package_data=True,
)
