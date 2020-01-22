from tsv         import format_fields
from csv         import reader
from json        import loads, dumps
from glob        import glob
from itertools   import product, combinations
from sqlite3     import connect
from os.path     import splitext, join
from collections import namedtuple


def csv_to_linear_tsv(csv_path):
    '''
    Function to convert csv file into linear-tsv file.

    TSV is very efficient for JS/Perl/Python to process, without losing any
    typing information, and also easy for humans to read. The format has been
    supported in 4store since its public release, and it's reasonably widely used.

    CSV is for loading into spreadsheets
    TSV is for processing by bespoke softwares.

    Arguments:
        csv_path: file path containing csv file.
    '''
    with open(csv_path, 'r') as csvfile:
        with open(splitext(csv_path)[0] + '.tsv', 'w') as tsvfile:
            for record in reader(csvfile):
                tsvfile.write(format_fields(record) + '\n')


def file_split(file_path, parts=10):
    '''
    Function to split given txt or csv file into given number of parts.

    Arguments:
        file_path: path of csv or txt file (any text document)
        parts: number of parts to split into (default=10)
    '''
    def chunks(ids, parts):
        for i in range(0, len(ids), parts):
            yield ids[i:i+parts]

    with open(file_path, 'r') as f:
        _file, _ext = splitext(file_path)
        _id = [x.strip() for x in f.readlines() if x]
        if not _id:
            return 'Empty file!'
        _no = len(_id) // parts
        val = chunks(_id, _no)
        for i, v in enumerate(val):
            with open('{}_{}{}'.format(_file, i, _ext), 'w') as f:
                f.write('\n'.join(v))


def merge_sqlite_db(folder_path, recursive=False, extension='sqlite3'):
    '''
    Function to merge multile sqlite db files into one db of same schema

    Arguments:
        folder_path: path containing all the sqlite files
        recursive: if you want to recursively find files from all the directory in given directory.
        extension: defaul is sqlite3 it could also be '.db'
    Return:
        final db path where all the db are merged
    '''
    _db_files = glob(join(folder_path, '*.{}'.format(extension)))
    if recursive:
        _db_files = glob(join(folder_path, '**/*.{}'.format(extension)), recursive=True)

    if not _db_files:
        return False
    if len(_db_files) == 1:
        return _db_files[0]

    if len(_db_files) > 1:
        final_db = _db_files[0]
        other_db = _db_files[1:]
        conn     = connect(final_db)
        curs     = conn.cursor()
        tables   = curs.execute('SELECT name FROM sqlite_master WHERE type="table";').fetchall()
        tables   = [x[0] for x in tables]

        for tablename in tables:
            headers = [x[0] for x in (curs.execute('SELECT * FROM %s' % tablename)).description]
            conn.close()

            for db in other_db:
                conn  = connect(db)
                curs  = conn.cursor()
                title = ','.join(headers)
                curs.execute('ATTACH DATABASE ? as main_db', (final_db,))
                curs.execute('INSERT OR IGNORE INTO {} SELECT {} FROM {}'.format('main_db.'+tablename, title, tablename))
                conn.commit()
        conn.close()
        return final_db

def get_string_product(string, length):
    '''
    Function to gererate product of given string of given length
    eg: get_string_product('123', 2) -> ['11', '12', '13', '21', '22', '23', '31', '32', '33']

    Arguments:
        string: character string eg: 'abcdef'
        length: 3
    Return:
        product of given string
    '''
    products = []
    for item in product(string, repeat=length):
        products.append(''.join(item))
    return products

def get_string_combinations(string, length):
    '''
    Function to generate combination of the given string of given length
    eg: get_string_combinations('123', 2) -> ['12', '13', '23']

    Arguments:
        string: character string eg: 'abcdef'
        length: 3
    Return:
        product of given string
    '''
    combination = []
    for item in combinations(string, length):
        combination.append(''.join(item))
    return combination

def dict_to_object(data):
    '''
    Function to create object out of a given dictionary/json dumps etc.
    eg: INPUT: {'a': {'b': {'c': 'd'}}} => OUTPUT: data(a=data(b=data(c='d')))
    Input:
        data: takes dictionary or json dump
    Return:
        namedtuple object which can be accessed like object
    '''
    data = dumps(data) if isinstance(data, dict) else data
    return loads(data, object_hook=lambda d: namedtuple('data', d.keys())(*d.values()))
