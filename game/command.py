from .interfaces import Renderable


class Command:
    """Command class for all commands"""


class RemoveInstanceCMD(Command):
    """Command for removing an instance"""

    def __init__(self, instance):
        self.instance = instance


class RemoveCallbackCMD(Command):
    """Command for removing a callback"""

    def __init__(self, callback, instance, type):
        self.callback = callback
        self.instance = instance
        self.type = type


class AddInstanceCMD(Command):
    """Command for adding an instance"""

    def __init__(self, instance):
        self.instance = instance


commands: list[Command] = []


def issue_command(cmd: Command) -> None:
    commands.append(cmd)
