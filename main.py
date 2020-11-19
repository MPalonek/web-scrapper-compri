from argparse import ArgumentParser
import logging
import json
import os
from datetime import date
import GenericScrapper

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-d", "--debug", '--DEBUG', action='store_true', help="set logging to be debug")
    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    log_filename = "wscp_log_0.log"
    logging.basicConfig(filename=log_filename, format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=loglevel)
    if os.path.isfile(log_filename):
        f = open(log_filename, "a")
        f.write("\n-----------------------------------------------------------------\n\n")
        f.close()
    logging.info('Starting Web Scrapper Compare Price. Current date is: {}'.format(date.today()))

    conn = GenericScrapper.create_connection("db/comprisqlite.db")
    GenericScrapper.create_tables(conn)
    GenericScrapper.insert_product(conn, "ryzen 5 3600x", 1119, "morele", "cpu", 5)
    GenericScrapper.insert_product(conn, "nvidia rtx 3090", 7200, "morele", "gpu")
    GenericScrapper.insert_product(conn, "ryzen 5 3600x", 1219, "x-kom", rating=3)
    GenericScrapper.insert_product(conn, "amd rx6900", 8099, "x-kom")
    conn.commit()


if __name__ == "__main__":
    main()
