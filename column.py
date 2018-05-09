"""
@author: frndlytm
@name: metamigrate.column
@description:
    Manages the attributes of a column in a table. Since the table manages the template,
    we only care about encoding the metadata consistently.
"""
class ColumnFactory:
    def make_column(self, position, name, columntype, nullable=1, default=None):
        return Column(
            position, name, columntype, self.convert_nullable(nullable), default
        )

    def convert_nullable(self, nullable):
        if nullable in [0, 1]: return nullable
        elif nullable == 'YES': return 1
        elif nullable == 'NO': return 0
        else: raise ValueError



class Column:
    def __init__(self, position, name, columntype, nullable, default):
        self._position = position
        self.name = name
        self.columntype = columntype
        self.nullable = nullable
        self.default = default

    def __repr__(self):
        return str(dict(
            name = self.name,
            columntype = self.columntype,
            nullable = self.nullable,
            default = self.default
        ))

    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, x):
        self._position = x

