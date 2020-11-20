import configparser

from download import download
from upload import upload

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    print(10 * '-', 'downloading', 10 * '-', sep='')
    download(config)
    print(10 * '-', 'uploading', 10 * '-', sep='')
    upload(config)
