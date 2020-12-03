import time
import json
import logging
import argparse
import docker

from pathlib import Path
from getmac import get_mac_address


def parse_args():
    parser = argparse.ArgumentParser(
        description='Start ap from docker')

    parser.add_argument('-c', '--config',
                        help='configure file name',
                        required=False,
                        type=str)

    return parser.parse_args()


def create_logger() -> logging.Logger:
    log_path = Path(__file__).parent.absolute() / 'logs'
    log_path.mkdir(parents=True, exist_ok=True)
    log_path = log_path / (time.strftime('%Y-%m-%d-%H-%M') + '.log')

    fh = logging.FileHandler(str(log_path))
    fh.setFormatter(logging.Formatter(
        '[%(levelname)s] %(asctime)s: %(message)s',
        datefmt='%Y-%m-%d_%H:%M:%S'))

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(fh)
    return logger


def check_wlan_status(cfg: dict):
    mac = get_mac_address(interface=cfg['kwargs']['environment']['INTERFACE'])
    
    if mac is None:
        return False
    else:
        ssid = mac.replace(':', '-')[-5:]
        cfg['kwargs']['environment']['SSID'] += ('_' + ssid)
        return True


def start_docker(cfg: dict, logger: logging.Logger):
    client = docker.from_env()
    result = client.containers.run(
        cfg['image'],
        **cfg['kwargs']
    )

    logger.info('\nDocker exit with message :\n' + result.decode('utf-8'))


def main():
    # time.sleep(10)

    args = parse_args()

    if args.config is None:
        args.config = Path(__file__).parent.absolute() / 'config.json'

    with open(args.config) as json_file:
        cfg = json.load(json_file)

    logger = create_logger()
    logger.info(f'\nload json: {args.config}\n{cfg}')

    if check_wlan_status(cfg):
        logger.info('\nRead interface success: {}'
                    '\nReady to start ap'
                    '\nSSID: {}'
                    '\nPassword: {}'.format(
                        cfg['kwargs']['environment']['INTERFACE'],
                        cfg['kwargs']['environment']['SSID'],
                        cfg['kwargs']['environment']['WPA_PASSPHRASE']
                    ))

        start_docker(cfg, logger)
    else:
        logger.info('\nCannot read interface: {}'
                    .format(cfg['kwargs']['environment']['INTERFACE']))


if __name__ == '__main__':
    main()
