"""
Setup configuration for the Omics AI Explorer Python library.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="omics-ai-explorer",
    version="0.1.0",
    author="DNAstack",
    author_email="support@dnastack.com",
    description="Python client library for Omics AI Explorer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dnastack/omics-ai-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
    },
    keywords="genomics bioinformatics omics explorer api client",
    project_urls={
        "Bug Reports": "https://github.com/dnastack/omics-ai-cli/issues",
        "Source": "https://github.com/dnastack/omics-ai-cli",
        "Documentation": "https://github.com/dnastack/omics-ai-cli#readme",
    },
)