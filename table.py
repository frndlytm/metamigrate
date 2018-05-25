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

    def make(self, name, fields=[], constraints={'check':[], 'primary key':[], 'foreign key':[]}):
        template = self.env.get_template(join(self.flavor,'create.j2'))
        return Table(template, name, fields, constraints)


class Table:
    def __init__(self, template, name, fields, constraints):
        self.template = template
        self.name = name
        self.fields = fields
        self.constraints = constraints

    def __repr__(self):
        return self.template.render(
            {
                'name': self.name,
                'fields': self.fields,
                'constraints': self.constraints
            }
        )

    def add_field(self, field):
        self.fields.append(field)

    def add_constraint(self, cons, cons_type):
        try:
            self.constraints[cons_type].append(cons)
        except:
            raise KeyError
