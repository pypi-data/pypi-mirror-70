"""
A koji wrapper
"""
from subprocess import STDOUT, check_output, CalledProcessError

class KojiCommandError(Exception):
    """Raised when Koji command fails"""
    def __init__(self, message, command):
        self.message = message
        self.command = command
        super(KojiCommandError, self).__init__(message)

def koji(command, executable=None):
    """
    Run a koji command
    """
    if executable is None:
        executable = 'koji'

    try:
        return check_output([executable] + command, stderr=STDOUT, universal_newlines=True)
    except CalledProcessError as error:
        raise KojiCommandError(error.output, error.cmd)
