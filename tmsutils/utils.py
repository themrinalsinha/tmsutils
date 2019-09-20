from tsv     import format_fields
from csv     import reader
from glob    import glob
from sqlite3 import connect
from os.path import splitext, join


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
