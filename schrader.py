import argparse
import logging
from modules import config, host, file_opener

LOG: logging.Logger = logging.getLogger('schrader')

def main(flags: argparse.Namespace):
    source: str = 'file'
    source_file: str = 'config.txt'
    inventory_file_name: str = 'inventory.lst'
    if flags.source != None:
        source = str(flags.source)
    if flags.file != None:
        source_file = str(flags.file)
    if flags.inventory != None:
        inventory_file_name = flags.inventory
    config_file: config.Config = config.Config(source=source, source_file=source_file)
    inventory: list[str] = parse_inventory(inventory_file_name)
    discover_host(config_file, inventory)

def parse_inventory(inventory_file_name: str) -> list[str]:
    inventory: list[str] = []
    inventory_file: str | None = file_opener.open_file(inventory_file_name)
    if inventory_file != None:
        inventory = inventory_file.split('\n')
    return inventory

def discover_host(config_file: config.Config, inventory: list[str]) -> list[host.Host]:
    LOG.info('Gathering information')
    discovered_hosts: list[host.Host] = []

    discovered_hosts.append(host.Host(config_file, '127.0.0.1', True))
    for host_address in inventory:
        if host_address != '':
            discovered_host = host.Host(config_file, host_address)
            discovered_hosts.append(discovered_host)
    LOG.info('Discovering hosts done. total hosts: {0}'.format(len(discovered_hosts)))

    return discovered_hosts

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Schrader',
        description='Schrader is a python library to gather remote host information'
    )
    parser.add_argument('-s', '--source')
    parser.add_argument('-f', '--file')
    parser.add_argument('-i', '--inventory')
    flags: argparse.Namespace = parser.parse_args()
    main(flags)