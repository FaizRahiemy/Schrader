import logging
import os
from modules import file_opener

LOG: logging.Logger = logging.getLogger('schrader')
LOG.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)

class Config():
    username: str
    password: str
    key_file_name: str

    def __init__(self, source: str='file', source_file: str='config.txt') -> None:
        LOG.debug(f'Getting credentials from: {source}')
        LOG.debug(f'Source file: {source_file}')
        if source == 'file':
            cred_file: str|None = file_opener.open_file(source_file)
            if cred_file == None:
                LOG.exception('Getting credentials file error')
            else:
                creds: list[str] = cred_file.split('\n')
                self.username = creds[0].split('=')[1]
                self.password = creds[1].split('=')[1]
                self.key_file_name = creds[2].split('=')[1]
        elif source == 'env':
            self.username = os.getenv('SCHRADER_USERNAME') # type: ignore
            self.password = os.getenv('SCHRADER_PASSWORD') # type: ignore
            self.key_file_name = os.getenv('SCHRADER_KEY_FILE') # type: ignore
        LOG.debug(f'username: {self.username}')
        LOG.debug(f'password len: {len(self.password)}')
        LOG.debug(f'key_file_name file: {self.key_file_name}')