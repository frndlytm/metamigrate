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


class ModelManager:
    #
    # A container for our connection information and for
    # selecting all data from a table.
    #
    def __init__(self, flavor, server, database, driver, port, schema):
        """
        Establish the connection data.
        """
        self.flavor = flavor
        self.server = server
        self.database = database
        self.driver = driver
        self.port = port
        self.schema = schema
        self._connection = None
        self._model = None


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
    # model is queried to the object on __enter__ through
    # the _setup() function.
    #
    @property
    def model(self):
        return self._model
    @model.setter
    def model(self, m):
        self._model = m

    #
    # enable context manager syntex for the MetaManager connection.
    #
    def __enter__(self):
        self.connection = create_engine(str(self))
        self._setup()
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
    # Helper for __enter__ to get all the meta data from the
    # tracked schema.
    #
    def _setup(self):
        if self.connection:
            self.model = (
                pd.read_sql_table(
                    '_Model', self.connection, schema=self.schema
                )
            )

    def tables(self):
        # query information_schema.
        attributes = ['TABLE_CATALOG', 'TABLE_SCHEMA', 'TABLE_NAME']
        tables = self.model[attributes].drop_duplicates(keep='last')
        return tables.to_records()

    def columns(self, table=None):
        # query information_schema.
        attributes = [
            'ORDINAL_POSITION', 'COLUMN_NAME', 'DATA_TYPE', 'IS_NULLABLE', 'COLUMN_DEFAULT'
        ]
        if table:
            columns = self.model[self.model['TABLE_NAME'] == table][attributes]
        else:
            columns = self.model[attributes]
        return columns.to_records()
