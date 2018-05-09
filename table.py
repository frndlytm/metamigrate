"""
@author: frndlytm
@name: metamigrate.table
@description:
    Given a set of columns and their meta data, can represent itself as a
    CREATE TABLE statement.

    It does this by leveraging a template file; however, this could be a
    decision based on the "flavor" of database engine being created.
"""
from os.path import join

class TableFactory:
    def __init__(self, env, flavor):
        self.env = env
        self.flavor = flavor

    def make_table(self, name):
        template = self.env.get_template(join(self.flavor,'create.j2'))
        return Table(template, name, None, None)


class Table:
    def __init__(self, template, name, columns, constraints):
        self.template = template
        self.name = name
        self.columns = columns
        self.constraints = constraints

    def __repr__(self):
        return self.template.render(
            {
                'name': self.name,
                'columns': sorted(self.columns, key=lambda column: column.position),
                'constraints': self.constraints
            }
        )

    def add_column(self, column):
        self.columns.append(column)

    def add_constraint(self, constraint):
        self.constraints.append(constraint)
