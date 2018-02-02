import csv
import os
import re
import shutil
import logging
import logging.config
import logging_config
import configparser
from icrawler.builtin import GoogleImageCrawler, FlickrImageCrawler

logging.config.dictConfig(logging_config.DEV)
log = logging.getLogger(__name__)

CSV_FOLDER = '{}/classification_csv'.format(os.getcwd())
IMAGE_FOLDER = '{}/classification_image'.format(os.getcwd())
USERDATA_CONF = '{}/userdata.conf'.format(os.getcwd())
FLICKR_KEY = ''


def csv_parser(csv_path):
    with open(csv_path, newline='') as csv_file:
        try:
            dialect = csv.Sniffer().sniff(csv_file.read())
            csv_file.seek(0)
        except csv.Error as e:
            raise('csv file ({}) format error: {}'.format(csv_path, e))

        reader = csv.reader(csv_file, dialect)
        next(reader)

        result = list()
        for row in reader:
            csv_row = list()
            csv_row.append(row[0])
            csv_row.append(row[1])

            result.append(csv_row)

        return result  # two dimensional array


def google_crawler(keyword, classification_folder):
    crawler = GoogleImageCrawler(parser_threads=2, downloader_threads=4, storage={'root_dir': classification_folder})
    crawler.crawl(keyword=keyword, max_num=500, file_idx_offset='auto')


def flickr_crawler(keyword, classification_folder):
    try:
        crawler = FlickrImageCrawler(FLICKR_KEY, parser_threads=2, downloader_threads=4, storage={'root_dir': classification_folder})
        crawler.crawl(max_num=500, text=keyword, sort='relevance', media='photos', per_page=500, file_idx_offset='auto')
    except Exception as e:
        log.error(e)


def download_image(keywords):
    for k in keywords:  # keywords: [['食物', '巧克力醬'], ['食物', '貝果']]
        if not k[0] or not k[1]:
            continue

        classification_folder = '{}/{}'.format(IMAGE_FOLDER, k[0])
        if not os.path.exists(classification_folder):
            os.makedirs(classification_folder)

        google_crawler(k[1], classification_folder)
        if FLICKR_KEY:
            flickr_crawler(k[1], classification_folder)


def crawler():
    log.debug('crawler start.')
    if not os.listdir(CSV_FOLDER):
        log.debug('classification_csv folder can not find csv file')
        return

    config = configparser.ConfigParser()
    config.read(USERDATA_CONF)
    global FLICKR_KEY
    FLICKR_KEY = config['System']['FlickrKey']

    for f in os.listdir(CSV_FOLDER):
        file_name = os.path.splitext(f)
        if file_name[1] != '.csv':
            log.warning('file name: {}, not a csv file'.format(f))
            continue

        csv_path = '{}/{}'.format(CSV_FOLDER, f)
        keywords = csv_parser(csv_path)
        download_image(keywords)

    log.debug('crawler done.')


if __name__ == '__main__':
    crawler()
