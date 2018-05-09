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
    #
    # A container for our connection information and for
    # selecting all data from a table.
    #
    def __init__(self, flavor, server, database, driver, port, env):
        """
        Establish the connection data.
        """
        self.flavor = flavor
        self.server = server
        self.database = database
        self.driver = driver
        self.port = port
        self._connection = None
        self.factory = TableFactory(env, flavor)

    #
    # connection is opened like a context manager through
    # __enter__ and closed through __exit__.
    #
    @property
    def connection(self):
        return self._connection
    @connection.setter
    def connection(self, conn):
        self._connection = conn


    #
    # enable context manager syntex for the MetaManager connection.
    #
    def __enter__(self):
        self.connection = create_engine(str(self))
        return self

    def __exit__(self, *args):
        self.connection.dispose()


    #
    # serialize the MetaManager as a connection string. Enables using
    # str(self) in the __enter__ method.
    #
    def __str__(self):
        return '{}+pyodbc:///?odbc_connect={}'.format(self.flavor, self._params())

    #
    # helper for __str__ to simplify the connection string.
    #
    def _params(self):
        return quote_plus(
            'DRIVER={};PORT={};SERVER={};DATABASE={};Trusted_Connection=yes;'
            .format(self.driver, self.port, self.server, self.database)
        )

    #
    # standard SQL operation on a database. Might want to revise this to
    # be more restrictive on a per-project schema.
    #
    def select_all(self, table, ordering=None):
        """
        Select all data from a table on the connection.
        """
        if ordering:
            ordering = ' ORDER BY '+','.join(ordering)
        else:
            ordering = ''
        query = "select * from {0}{1}".format(table, ordering)
        data = pd.read_sql(query, self.connection)
        return data