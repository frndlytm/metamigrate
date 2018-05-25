"""
@author: frndlytm
@name: metamigrate.column
@description:
    Manages the attributes of a column in a table. Since the table manages the template,
    we only care about encoding the metadata consistently.
"""
class FieldFactory:
    def make(self, position, name, data_type, is_nullable=True, default=None):
        return dict(
            position=position,
            name=name,
            data_type=data_type,
            is_nullable=self.convert_nullable(is_nullable),
            default=default
        )

    def convert_nullable(self, nullable):
        if isinstance(nullable, bool): return nullable
        elif nullable == 'YES' or nullable == 1: return True
        elif nullable == 'NO' or nullable == 0: return False
        else: raise ValueError


