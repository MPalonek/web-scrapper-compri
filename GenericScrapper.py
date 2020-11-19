import sqlite3
from sqlite3 import Error
import logging

# https://www.sqlitetutorial.net/sqlite-python/
# https://stackoverflow.com/questions/10325683/can-i-read-and-write-to-a-sqlite-database-concurrently-from-multiple-connections


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logging.info('Connected to database. SQlite version {}, sqlite adapter module version {}'.format(sqlite3.sqlite_version, sqlite3.version))
    except Error as e:
        logging.error('Failed to connect to database. {}'.format(e))

    return conn


def execute_command(conn, command):
    """ execute command statement
    :param conn: Connection object
    :param command: sqlite statement
    :return:
    """
    try:
        c = conn.cursor()
        logging.debug('Executing command: {}'.format(command))
        c.execute(command)
    except Error as e:
        logging.error('Failed to execute command. {}'.format(e))


def create_tables(conn):
    """ create tables for database (systemInfo, products) and insert current version entry
    :param conn: Connection object
    :return:
    """
    try:
        systemInfo = "CREATE TABLE IF NOT EXISTS systemInfo (creationDate date DEFAULT CURRENT_TIMESTAMP PRIMARY KEY, version integer NOT NULL);"
        systemInfoEntry = "INSERT INTO systeminfo (version) VALUES (1);"
        products = "CREATE TABLE IF NOT EXISTS products (id integer PRIMARY KEY AUTOINCREMENT, name text NOT NULL, price real NOT NULL, date date DEFAULT CURRENT_DATE, shopName text NOT NULL, category text, rating real);"
        commands = [systemInfo, systemInfoEntry, products]
        for cmd in commands:
            execute_command(conn, cmd)
        conn.commit()
    except Error as e:
        logging.error('Failed to create tables. {}'.format(e))


def insert_product(conn, name, price, shopName, category=None, rating=None):
    """ insert entry to product table
        :param conn: Connection object
        :param name:
        :param price:
        :param shopName:
        :param category:
        :param rating:
        :return:
        """
    try:
        if category == None and rating == None:
            insert = 'INSERT INTO products(name, price, shopName) VALUES("{}", {}, "{}");'.format(name, price, shopName)
        elif category == None:
            insert = 'INSERT INTO products(name, price, shopName, rating) VALUES("{}", {}, "{}", {});'.format(name, price, shopName, rating)
        elif rating == None:
            insert = 'INSERT INTO products(name, price, shopName, category) VALUES("{}", {}, "{}", "{}");'.format(name, price, shopName, category)
        else:
            insert = 'INSERT INTO products(name, price, shopName, category, rating) VALUES("{}", {}, "{}", "{}", {});'.format(name, price, shopName, category, rating)
        execute_command(conn, insert)
    except Error as e:
        logging.error('Failed to insert entry. {}'.format(e))
