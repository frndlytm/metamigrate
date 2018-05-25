"""
@author: frndlytm
@name: metamigrate.column
@description:
    Manages the attributes of a column in a table. Since the table manages the template,
    we only care about encoding the metadata consistently.

    NOTE: Had a problem with numpy.recarray
"""
class FieldFactory:
    def make(self, record):
        return dict(
            position=record[1],
            name=record[2],
            data_type=record[3],
            is_nullable=self._convert_nullable(record[4]),
            default=record[5]
        )


    # def _make(self, position, name, data_type, is_nullable=True, default=None):
    #     #
    #     # standard Field __repr__ is a dict for the
    #     # Table template to consume
    #     #
    #     return dict(
    #         position=position,
    #         name=name,
    #         data_type=data_type,
    #         is_nullable=self._convert_nullable(is_nullable),
    #         default=default
    #     )

    def _convert_nullable(self, nullable):
        #
        # serialize is_nullable to True or False.
        #
        if isinstance(nullable, bool): return nullable
        elif nullable == 'YES' or nullable == 1: return True
        elif nullable == 'NO' or nullable == 0: return False
        else: raise ValueError


    def _from_array(self, arr):
        #
        # If introspection yeilds a list, assume
        # it's ordered correctly and make a field.
        # This may be a bad assumption, but ModelManager
        # handles the ordering upstream.
        #
        pass


