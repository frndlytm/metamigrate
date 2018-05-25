"""
@author: frndlytm
@name: metamigrate.column
@description:
    Manages the attributes of a column in a table. Since the table manages the template,
    we only care about encoding the metadata consistently.
"""
class FieldFactory:
    def make(self, record):
        if isinstance(record, dict):
            return record
        elif isinstance(record, tuple) or isinstance(record, list):
            return self._from_tuple(record)
        # elif isinstance(record, str):
        #   do split_by_delimiter(introspect=True)
        else:
            return

    def _make(self, position, name, data_type, is_nullable=True, default=None):
        return dict(
            position=position,
            name=name,
            data_type=data_type,
            is_nullable=self._convert_nullable(is_nullable),
            default=default
        )

    def _convert_nullable(self, nullable):
        if isinstance(nullable, bool): return nullable
        elif nullable == 'YES' or nullable == 1: return True
        elif nullable == 'NO' or nullable == 0: return False
        else: raise ValueError

    def _from_tuple(self, tup):
        return self._make(
            tup[1],     # position
            tup[2],     # name
            tup[3],     # data_type
            tup[4],     # is_nullable
            tup[5]      # default
        )

