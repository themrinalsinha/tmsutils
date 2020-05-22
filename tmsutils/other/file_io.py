from json       import loads
from os.path    import exists, join
from requests   import get
from subprocess import check_output, STDOUT

class FileIO(object):
    '''
    Module to share and send files to someone with a temporary link
    for one time use, you can also set the expiry along with it
    eg: '1w', '7 days', '14 days'
    '''
    def upload(self, file_path, expiry='1w', timeout=120):
        '''
        NOTE: This function uses 'curl' function on command line
              so make sure you have curl installed on command line.
        This function uploads given file to file.io and returns download url and status
        Arguments:
            file_path - file which you want to uplaod
            expiry    - download link expiry
            timeout   - shell timeout
        '''
        fileio_domain = 'https://file.io/?expires={}'.format(expiry)
        if not exists(file_path):
            return False
        command = 'curl -F "file=@{}" {}'.format(file_path, fileio_domain)
        output  = check_output(command, stderr=STDOUT, timeout=timeout, shell=True)
        output  = output.decode('utf-8').rsplit('\n')[-1]
        return loads(output)

    def download(self, download_url, location):
        '''
        Download function downloads given fileIO url to given location
        Arguments:
            download_url - download url from file.io eg: ('https://file.io/ouJEmh')
            location     - wherever in the system you want to download it
        Returns:
            downloaded filepath in case of download or none if file not found
        '''
        try:
            with get(download_url, stream=True) as resp:
                file_name = resp.headers['Content-disposition'].split(';')[-1].split('=')[-1]
                if not file_name:
                    return
                with open(join(location, file_name), 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
            return join(location, file_name)
        except:
            return
