import logging
import paramiko
import socket
from modules import config, file_opener

LOG: logging.Logger = logging.getLogger('schrader')
LOG.setLevel(logging.DEBUG)

class Host():
    config_file: config.Config
    ip_address: str = ''
    hostname: str = ''
    os_name: str = ''
    os_version: str = ''
    os_comply: bool = False
    client: paramiko.SSHClient|None

    def __init__(self, config_file: config.Config, ip_address: str, is_scanner: bool = False):
        self.config_file = config_file
        self.ip_address = ip_address

        if is_scanner:
            LOG.debug('Getting own info')
            try:
                self.hostname: str = socket.gethostname()
            except:
                self.hostname = 'Unknown'
                
            self.ip_address = '127.0.0.1'
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(('192.255.255.255', 1))
                self.ip_address = s.getsockname()[0]
            finally:
                s.close()

            try:
                os_name, os_version = self.get_os_information(file_opener.open_file_wildcard('/etc/*release'))
            except:
                os_name = os_version = 'Unknown'

            self.os_name = os_name
            self.os_version = os_version
            self.os_comply = self.is_os_comply()
        else:
            LOG.debug(f'Discovering {ip_address}')
            self.connect_host()
            if self.client != None:
                hostname_file: str = self.run_host_command('hostname')
                if len(hostname_file.split('\n')) > 1:
                    self.hostname = hostname_file.split('\n')[0]
                else:
                    self.hostname = hostname_file
                
                etc_release_file: str = self.run_host_command('cat /etc/*release')
                self.os_name, self.os_version = self.get_os_information(etc_release_file)
                self.os_comply = self.is_os_comply()
                self.touch_tmp()
                self.client.close()
        LOG.debug(f'hostname: {self.hostname}')
        LOG.debug(f'ip_address: {self.ip_address}')
        LOG.debug(f'os_name: {self.os_name}')
        LOG.debug(f'os_version: {self.os_version}')
        LOG.debug(f'os_comply: {self.os_comply}')

    def connect_host(self) -> paramiko.SSHClient|None:
        LOG.debug(f'connecting to: {self.ip_address}')
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            if self.config_file.key_file_name == '':
                self.client.connect(hostname=self.ip_address, username=self.config_file.username, password=self.config_file.password)
            else:
                self.client.connect(hostname=self.ip_address, username=self.config_file.username, password=self.config_file.password, key_filename=self.config_file.key_file_name)
        except Exception as e:
            self.client = None # type: ignore
            LOG.error(f'Connecting {self.ip_address} error')

    def run_host_command(self, command: str) -> str:
        LOG.debug(f'Running ssh command: {command}')

        output: str = ''
        if self.client != None:
            try:
                _, stdout, stderr = self.client.exec_command(command)
                output: str = stdout.read().decode()
                err: str = stderr.read().decode()
                if err:
                    LOG.debug(f'Running ssh command error: {err}')
                else:
                    LOG.debug(f'Command output: {output}')
            except Exception as e:
                LOG.error(f'Running ssh command error: {e}')

        return output
    
    def touch_tmp(self) -> None:
        LOG.debug(f'Touching /tmp/schrader')
        self.run_host_command('touch /tmp/schrader')

    def get_os_information(self, etc_release: str) -> tuple[str, str]:
        LOG.debug('Getting os information')
        etc_release_lines: list[str] = etc_release.split('\n')
        os_name = 'Unknown'
        os_version = 'Unknown'
        temp: str = ''
        for etc_release_line in etc_release_lines:
            if etc_release_line != '':
                temp = etc_release_line
            if 'PRETTY_NAME'.lower() in etc_release_line.lower():
                try:
                    os_name = etc_release_line.split('=')[1].replace('"', '')
                except:
                    os_name = etc_release_line
            if 'VERSION_ID'.lower() in etc_release_line.lower():
                try:
                    os_version = etc_release_line.split('=')[1].replace('"', '')
                except:
                    os_version = etc_release_line
        if os_name == 'Unknown' and temp != '':
            os_name = os_version = temp
        
        return os_name, os_version
    
    def is_os_comply(self) -> bool:
        if 'ubuntu' in self.os_name.lower():
            if '24' in self.os_version:
                return True
        return False