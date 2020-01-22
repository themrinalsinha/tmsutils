# tmsutils [![PyPI version](https://badge.fury.io/py/tmsutils.svg)](https://badge.fury.io/py/tmsutils) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/themrinalsinha/tmsutils/graphs/commit-activity) [![Build Status](https://travis-ci.org/TheMrinalSinha/tmsutils.svg?branch=master)](https://travis-ci.org/TheMrinalSinha/tmsutils)

collection of utility functions to make task easy

Function list:

- `csv_to_linear_tsv` - function to convert given csv file into linear tsv file
- `file_split` - function to split text or csv file into given chunks
- `merge_sqlite_db` - function to merge sqlite database file of same schema
- `get_string_product` - function to generate product of the given string of given length
- `get_string_combinations` - function to generate combination of the given string of given length
- `dict_to_object` - function to convert dictionary or json dump into object

Classes:
- `S3` (wrapper for S3 data storages)
    - `file_exists` - check if given key exists or not
    - `get_temperory_link` - get temperory download link for a given key
    - `upload` - upload your file or directory to s3 storage
    - `download` - download given key or entire folder from s3 storage

- `FileIO` (wrapper for https://file.io 'snapchat' of file sharing)
    - NOTE: it requires 'curl' commandline tool to be installed
    - `upload` - upload file to 'https://file.io' and returns file download link
    - `download` - download file from the given file.io url to given location

CLI (Commandline Utilities):
- `gi` (designed to help you create .gitignore files for your git repositories)
    - It is used to generate gitignore for `operating systems`, `IDEs`, or `Programming Languages`
    - The below command will generate .gitignore for python (PL) and code (IDE) in same place.
    ```
    $ tms gi python,code
    ```
    - In case of any such type which is not valid then
    ```
    $ tms gi python3,abcdx

    "python3" is invalid, try from "python"
    "abcdx" is invalid.
    ```
- `mdb` (merging sqlite database command)
    - It is used to merge sqlite3 database files
    ```
    Options:
        --path = default current directory from where comand runs
        --extension = default is set to sqlite, can also use 'db'

    It returns db file path if which all other are merged or return No file found.
    ```
- `sf` (splitting files (eg: txt, csv, tsv etc..) into equal chunks of given size)
    - takes file path as an arugument, it splits the file by default into 10 chunks
    ```
    Options:
        FILEPATH - path to the file
        --chunk, -c <int> number of chunks (default=10)
    ```
