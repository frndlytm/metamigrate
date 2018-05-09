"""
@author: frndlytm
@name: metamigrate.loader
@description:
    A loader maps the meta data in the form of tuples into objects.
    Consumes:
        .tables, as string
        .columns, as a tuples
        .columnfactory, consuming tuples from columns
        .tablefactory, consuming tuples from tables, and columns from columnfactory

    Yields:
        .table objects
"""

class Loader:
    def __init__(self, tables, columns, tablefactory, columnfactory):
        self.tables = tables
        self.columns = columns
        self.tablefactory = tablefactory
        self.columnfactory = columnfactory

    def load(self):
        tables = (self.tablefactory.make_table(table) for table in self.tables)
        for table in tables:
            columns = filter(lambda col: col[0] == table.name, self.columns)
            for column in columns:
                table.add_column(self.columnfactory(column[1]))
            yield table


