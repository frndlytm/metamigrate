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

class ModelFactory:
    def __init__(self, environment, flavor, fieldfactory):
        self.environment = environment
        self.flavor = flavor
        self.fieldfactory = fieldfactory

    def make(self, database, schema, name, fields=[], constraints=dict()):
        # get the template by flavor...
        template = self.environment.get_template(self.flavor+'/create.j2')

        # map a serialized format onto the fields...
        fields = [self.fieldfactory.make(f) for f in fields]

        # build the table.
        return Model(template, database, schema, name, fields, constraints)


class Model:
    def __init__(self, template, database, schema,  name, fields, constraints):
        self.template = template
        self.database = database
        self.schema = schema
        self.name = name
        self.fields = fields
        self.constraints = constraints

    def __repr__(self):
        return self.template.render(
            {
                'database': self.database,
                'schema': self.schema,
                'name': self.name,
                'fields': self.fields,
                'constraints': self.constraints
            }
        )

    def add_field(self, field):
        self.fields.append(field)

    def add_constraint(self, cons, cons_type):
        # Check that the constraints are okay.
        # This should be handled by flavor in
        # concrete models.
        valid_cons_types = ['check', 'primary key', 'foreign key']
        if cons_type in valid_cons_types:

            # If a similar constraint exists, append.
            if cons_type in self.constraints:
                self.constraints[cons_type].append(cons)

            # else, make a new list for it.
            else:
                self.constraints[cons_type] = [cons]

        # raise an error on invalid type
        else:
            raise KeyError
