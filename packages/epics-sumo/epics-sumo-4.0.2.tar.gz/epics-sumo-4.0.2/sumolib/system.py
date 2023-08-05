"""System utilities.
"""

# pylint: disable=C0103
#                          Invalid name for type variable

import os
import subprocess

__version__="4.0.2" #VERSION#

# -----------------------------------------------
# basic system utilities
# -----------------------------------------------

# standard set of environment variables here:
_new_env = dict(os.environ)

# Only on Unix-Like systems:
# Ensure that language settings for called commands are english, keep current
# character encoding:
if os.name=="posix" and "LANG" in _new_env:
    _l= _new_env["LANG"].split(".")
    if len(_l)==2:
        _l[0]= "en_US"
        _new_env["LANG"]= ".".join(_l)

def copy_env():
    """create a new environment that the user may change."""
    return dict(_new_env)

def system_rc(cmd, catch_stdout, catch_stderr, env, verbose, dry_run):
    """execute a command.

    execute a command and return the programs output
    may raise:
    IOError(errcode,stderr)
    OSError(errno,strerr)
    ValueError
    """
    # pylint: disable=too-many-arguments
    def to_str(data):
        """decode byte stream to unicode string."""
        if data is None:
            return None
        return data.decode()
    if dry_run or verbose:
        print(">", cmd)
        if dry_run:
            return (None, None, 0)
    if catch_stdout:
        stdout_par=subprocess.PIPE
    else:
        stdout_par=None

    if catch_stderr:
        stderr_par=subprocess.PIPE
    else:
        stderr_par=None
    if env is None:
        env= _new_env

    p= subprocess.Popen(cmd, shell=True,
                        stdout=stdout_par, stderr=stderr_par,
                        close_fds=True,
                        env= env
                       )
    (child_stdout, child_stderr) = p.communicate()
    # pylint: disable=E1101
    #         "Instance 'Popen'has no 'returncode' member
    return (to_str(child_stdout), to_str(child_stderr), p.returncode)

def system(cmd, catch_stdout, catch_stderr, env, verbose, dry_run):
    """execute a command with returncode.

    execute a command and return the programs output
    may raise:
    IOError(errcode,stderr)
    OSError(errno,strerr)
    ValueError
    """
    # pylint: disable=too-many-arguments
    (child_stdout, child_stderr, rc)= system_rc(cmd,
                                                catch_stdout, catch_stderr,
                                                env,
                                                verbose, dry_run)
    if rc!=0:
        # pylint: disable=no-else-raise
        if catch_stderr:
            raise IOError(rc,
                          "cmd \"%s\", errmsg \"%s\"" % (cmd,child_stderr))
        else:
            raise IOError(rc,
                          "cmd \"%s\", rc %d" % (cmd, rc))
    return (child_stdout, child_stderr)

program_tests= set()

def test_program(cmd):
    """test if a program exists."""
    if cmd in program_tests:
        # already checked
        return
    try:
        system(cmd+" --version", True, True, None, False, False)
    except IOError as e:
        if "not found" in str(e):
            raise IOError("Error, %s: command not found" % cmd)
        raise e
    program_tests.add(cmd)

def _test():
    """perform internal tests."""
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
