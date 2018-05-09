"""
@author: frndlytm
@name: metamigrate.manager
@description:
    Manages the connection properties, templating environment, and factories
    that all communicate.

    This is effectively a server that serves up table creation statements from
    some metadata.
"""
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from table import TableFactory


class MetaManager:
    """
    A container for our connection information and for
    selecting all data from a table.
    """
    def __init__(self, flavor, server, database, driver, port, env):
        """
        Establish the connection data.
        """
        self.flavor = flavor
        self.server = server
        self.database = database
        self.driver = driver
        self.port = port
        self.factory = TableFactory(env, flavor)


    def __enter__(self):
        """
        Connect to the database for querying.
        """
        self.conn = create_engine(str(self))
        return self

    def __exit__(self, *args):
        """
        Disconnect on wrap-up.
        """
        self.conn.dispose()

    def __str__(self):
        return '{}+pyodbc:///?odbc_connect={}'.format(self.flavor, self._params())

    def _params(self):
        return quote_plus(
            'DRIVER={};PORT={};SERVER={};DATABASE={};Trusted_Connection=yes;'
            .format(self.driver, self.port, self.server, self.database)
        )

    def select_all(self, table):
        """
        Select all data from a table on the connection.
        """
        query = "select * from {0}".format(table)
        data = pd.read_sql(query, self.conn)
        return data