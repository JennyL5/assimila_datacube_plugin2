import os.path as op
import yaml
from .dq_exceptions import DBError
import logging
from .setup_logger import SetUpLogger
import psycopg2
#import pandas as pd


class DqDbConnection:
    def __init__(self, connect_yaml=None):
        """
        Constructor
        - Attach to logger (create if necessary).
        - Open and read the database connection settings file.
        :param connect_yaml: if provided, the connection information is read from
        this file, defaults to None
        """
        self.dbconn = None
        self.dbcursor = None

        SetUpLogger.setup_logger(
            default_config=op.abspath(op.join(op.dirname(__file__),
                                              "./logging_config.yml")))
        self.logger = logging.getLogger("__main__")

        # Check whether we've been provided with connection information
        # otherwise use the local default file.
        connect_info_file = connect_yaml if connect_yaml else \
            op.abspath(op.join(op.dirname(__file__),
                               "dq_DB_conf/db_settings.yaml"))

        try:
            with open(connect_info_file, 'r') as f:
                self.connect_info = yaml.load(f)
        except IOError as e:
            err_msg = f"Unable to read database connection information file " \
                      f"{connect_info_file}\n{e}"
            self.logger.error(err_msg, exc_info=True)
            raise DBError(err_msg)

    def __del__(self):
        try:
            #self.logger = None
            self.close()
        except psycopg2.Error:
            # it doesn't matter if the close() has already been done and
            # another attempt throws an error.
            pass

    def connect(self):
        """
        Create a connection to the database and get a cursor for it.
        :return: no return
        """
        # Build connection string
        try:
            conn_str = ' '.join(
                    ["{}={}".format(key, value) for key, value in
                     self.connect_info.items()]
            )
            # Make connection to the database
            self.dbconn = psycopg2.connect(conn_str)
            # Create the database cursor
            self.dbcursor = self.dbconn.cursor()

        except AttributeError as e:
            if not e.args:
                e.args = tuple()
            e.args += ('Unable to ingest database config information',)
            raise
        except psycopg2.Error as e:
            err_msg = f'Unable to make connection with database. Check db ' \
                      f'connection settings file:\n{e}'
            self.logger.error(err_msg, exc_info=True)
            raise DBError(err_msg)

    def do(self, sql_command):
        """
        Execute the sql command.
        :param sql_command: SQL syntax query
        :return: no return
        """
        try:
            self.dbcursor.execute(sql_command)
            # Commit the changes
            self.dbconn.commit()

        except psycopg2.Error as e:
            err_msg = f'Unable to execute command {sql_command}\n{e}'
            self.logger.error(err_msg)
            raise DBError(err_msg)

    def get(self, sql_command):
        """
        Execute the sql command and return the result.
        :param sql_command: SQL syntax query
        :return: Result of query as list (rows) of tuples (items in row)
        """
        try:
            self.dbcursor.execute(sql_command)
        # return the response
        # The method fetches all (or all remaining) rows of a query result set
        # and returns a list of tuples. If no more rows are available, it
        # returns an empty list.
            return self.dbcursor.fetchall()

        except psycopg2.Error as e:
            err_msg = f'Unable to execute command: {sql_command}\n{e}'
            self.logger.error(err_msg)
            raise DBError(err_msg)
        except IndexError as e:
            err_msg = f'Unable to fetch result from: {sql_command}\n{e}'
            self.logger.error(err_msg)
            raise DBError(err_msg)

    def get_df(self, sql_command):
        """
        Execute the sql command and return the result.
        :param sql_command: SQL syntax query
        :return: pandas DataFrame containing the result.
        """
        try:
            return pd.read_sql(f"{sql_command}", con=self.dbconn)

        except psycopg2.Error as e:
            err_msg = f'Unable to execute command: {sql_command}\n{e}'
            self.logger.error(err_msg)
            raise DBError(err_msg)

    def close(self):
        """
        Close the cursor and database connection
        :return: no return
        """
        # Close connection to database
        self.dbcursor.close()
        self.dbconn.close()
        self.logger.debug('Close connection to DQ database.')