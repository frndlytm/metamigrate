"""
@author: frndlytm
@name: metamigrate.column
@description:
    Manages the attributes of a column in a table. Since the table manages the template,
    we only care about encoding the metadata consistently.
"""

class Column:
    def __init__(self, position, name, columntype, nullable=1, default=None):
        self.position = position
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

    def get_position(self):
        return self.position