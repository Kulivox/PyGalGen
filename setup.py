import os
import setuptools

DESCRIPTION = "Toolkit used for generation and validation of Galaxy tool " \
              "definition files of python programs "
NAME = "pygalgen"
AUTHOR = "Michal Klinka"
AUTHOR_EMAIL = "mich.klinka@gmail.com"
MAINTAINER = "Michal Klinka"
MAINTAINER_EMAIL = "mich.klinka@gmail.com"
DOWNLOAD_URL = 'https://github.com/Kulivox/TRToolsTDFGenerator'
LICENSE = 'MIT'

VERSION = "0.3.0"


with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license_file="LICENSE",
    entry_points={
        'console_scripts': [
            'pygalgen=pygalgen.generator.main:run',
            'pygallint=pygalgen.linter.linter:run'
        ],
    },
    url=DOWNLOAD_URL,
    download_url=DOWNLOAD_URL,
    project_urls={
        "Bug Tracker": f"{DOWNLOAD_URL}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["lxml", "PyYAML"],
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
)