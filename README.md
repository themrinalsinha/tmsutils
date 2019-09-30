# tmsutils
collection of utility functions to make task easy

Function list:

- `csv_to_linear_tsv` - function to convert given csv file into linear tsv file
- `file_split` - function to split text or csv file into given chunks
- `merge_sqlite_db` - function to merge sqlite database file of same schema
- `get_string_product` - function to gererate product of the given string of given length
- `get_string_combinations` - function to generate combination of the given string of given length

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
