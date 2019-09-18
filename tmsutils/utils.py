from tsv     import format_fields
from csv     import reader
from os.path import splitext

def csv_to_linear_tsv(csv_path):
    '''
    Function to convert csv file into linear-tsv file.

    TSV is very efficient for JS/Perl/Python to process, without losing any
    typing information, and also easy for humans to read. The format has been
    supported in 4store since its public release, and it's reasonably widely used.

    CSV is for loading into spreadsheets
    TSV is for processing by bespoke softwares.
    '''
    with open(csv_path, 'r') as csvfile:
        with open(splitext(csv_path)[0] + '.tsv', 'w') as tsvfile:
            for record in reader(csvfile):
                tsvfile.write(format_fields(record) + '\n')

def file_split(file_path, parts=10):
    '''
    Function to split given txt or csv file into given number of parts.
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
                f.write('\n'.join(x for x in v))
