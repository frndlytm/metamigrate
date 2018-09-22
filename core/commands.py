"""
@name: metamigrate.core.commands
@auth: frndlytm@github.com
@desc:

    Commands follow the Command pattern from the original
    GoF Design Patterns book as a means of decoupling the
    execution logic from the model logic by enabling plug-
    in-styled Commands as objects attached to buttons or
    in the case of metamigrate, CLI commands.

    Ideally, the syntax for using metamigrate will be:
    
        > python metamigrate.py <command> <*options>

    This structure will offer an API to OS-agnostic CLIs
    for pushing models around and updating them. Further,
    this enables system-level scripting on metamigrate as
    a whole.
"""
from models import Model

class MigrateCommand:
    """MigrateCommands take a model to operate on, and run
    a sequence of database-driven steps on metadata exposed 
    by the model.
    """
    def __init__(self, model: Model) -> None:
        self.model = model
    def execute(self) -> None:
        raise NotImplementedError

class CreateCommand(MigrateCommand):
    def execute(self) -> None:
        pass

class DropCommand(MigrateCommand):
    def execute(self) -> None:
        pass

class BackupCommand(MigrateCommand):
    def execute(self) -> None:
        pass



class MigrateMacro(MigrateCommand):
    def __init__(self, model: Model, *commands: list) -> None:
        super.__init__(self, model)
        self.commands = commands

    def execute(self) -> None:
        assert self.commands
        for command in self.commands:
            command.execute()


