import glob
import logging

LOG = logging.getLogger('schrader')

def open_file(file_name: str) -> str | None:
    LOG.debug(f'Open file: {file_name}')
    results: str | None = None
    try:
        with open(file_name, 'r') as f:
            results = f.read()
    except Exception as e:
        LOG.exception(f'Error: {e}')
    return results

def open_file_wildcard(file_name: str) -> str:    
    results: str | None = ''
    for filename in glob.glob(file_name):
        with open(filename, 'r') as f:
            results += f.read()
    return results