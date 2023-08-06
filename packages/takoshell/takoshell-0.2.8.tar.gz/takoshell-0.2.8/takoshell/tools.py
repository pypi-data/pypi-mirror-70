# This file is part of tako
# Copyright (c) 2015-2017 Adam Hartz <hartz@mit.edu> and contributors
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# tako is a fork of xonsh (http://xon.sh)
# xonsh is Copyright (c) 2015-2016 the xonsh developers and is licensed under
# the 2-Clause BSD license.

# -*- coding: utf-8 -*-
"""Misc. tako tools.

The following implementations were forked from the IPython project:

* Copyright (c) 2008-2014, IPython Development Team
* Copyright (C) 2001-2007 Fernando Perez <fperez@colorado.edu>
* Copyright (c) 2001, Janko Hauser <jhauser@zscout.de>
* Copyright (c) 2001, Nathaniel Gray <n8gray@caltech.edu>

Implementations:

* decode()
* encode()
* cast_unicode()
* safe_hasattr()
* indent()

"""
import os
import re
import sys
import string
import builtins
import pathlib
import traceback
import subprocess
import collections
from glob import iglob
from warnings import warn
from subprocess import CalledProcessError
from collections import OrderedDict, Sequence, Set, abc

from takoshell.platform import scandir, DEFAULT_ENCODING, PYTHON_VERSION_INFO

IS_SUPERUSER = os.getuid() == 0


class TakoError(Exception):
    pass


class TakoCalledProcessError(TakoError, CalledProcessError):
    """Raised when there's an error with a called process

    Inherits from TakoError and subprocess.CalledProcessError, catching
    either will also catch this error.

    Raised *after* iterating over stdout of a captured command, if the
    returncode of the command is nonzero.

    Example:
        try:
            for line in !(ls):
                print(line)
        except CalledProcessError as error:
            print("Error in process: {}.format(error.completed_command.pid))

    This also handles differences between Python3.4 and 3.5 where
    CalledProcessError is concerned.
    """
    def __init__(self, returncode, command, output=None, stderr=None,
                 completed_command=None):
        super().__init__(returncode, command, output)
        self.stderr = stderr
        self.completed_command = completed_command


def expandpath(path):
    """
    Performs environment variable / user expansion on a given path
    if the relevant flag has been set.
    """
    env = getattr(builtins, '__tako_env__', os.environ)
    if env['TAKO_SETTINGS'].expand_env_vars:
        # expand variables and use os.path.abspath to handle cases
        # with relative paths like ../ or ./
        path = os.path.expanduser(expandvars(path))
    return path


def decode_bytes(path):
    """
    Tries to decode a path in bytes using TAKO_ENCODING if available,
    otherwise using sys.getdefaultencoding().
    """
    env = builtins.__tako_env__
    settings = env['TAKO_SETTINGS']
    return path.decode(encoding=settings.encoding,
                       errors=settings.encoding_errors)


class EnvPath(collections.MutableSequence):
    """
    A class that implements an environment path, which is a list of
    strings. Provides a custom method that expands all paths if the
    relevant env variable has been set.
    """
    def __init__(self, args=None):
        if not args:
            self._l = []
        else:
            if isinstance(args, str):
                self._l = args.split(os.pathsep)
            elif isinstance(args, pathlib.Path):
                self._l = [args]
            elif isinstance(args, bytes):
                # decode bytes to a string and then split based on
                # the default path separator
                self._l = decode_bytes(args).split(os.pathsep)
            elif isinstance(args, collections.Iterable):
                # put everything in a list -before- performing the type check
                # in order to be able to retrieve it later, for cases such as
                # when a generator expression was passed as an argument
                args = list(args)
                if not all(isinstance(i, (str, bytes, pathlib.Path)) \
                                      for i in args):
                    # make TypeError's message as informative as possible
                    # when given an invalid initialization sequence
                    raise TypeError(
                            "EnvPath's initialization sequence should only "
                            "contain str, bytes and pathlib.Path entries")
                self._l = args
            else:
                raise TypeError('EnvPath cannot be initialized with items '
                                'of type %s' % type(args))

    def __getitem__(self, item):
        if isinstance(item, slice):
            return [expandpath(i) for i in self._l[item]]
        return expandpath(self._l[item])

    def __setitem__(self, index, item):
        self._l.__setitem__(index, item)

    def __len__(self):
        return len(self._l)

    def __delitem__(self, key):
        self._l.__delitem__(key)

    def insert(self, index, value):
        self._l.insert(index, value)

    @property
    def paths(self):
        """
        Returns the list of directories that this EnvPath contains.
        """
        return list(self)

    def __repr__(self):
        return repr(self._l)

    def __str__(self):
        return os.pathsep.join(self._l)



class DefaultNotGivenType(object):
    """Singleton for representing when no default value is given."""


DefaultNotGiven = DefaultNotGivenType()

BEG_TOK_SKIPS = frozenset(['WS', 'INDENT', 'NOT', 'LPAREN'])
END_TOK_TYPES = frozenset(['SEMI', 'AND', 'OR', 'RPAREN'])
RE_END_TOKS = re.compile('(;|and|\&\&|or|\|\||\))')
LPARENS = frozenset(['LPAREN', 'AT_LPAREN', 'BANG_LPAREN', 'DOLLAR_LPAREN',
                     'ATDOLLAR_LPAREN'])


def _is_not_lparen_and_rparen(lparens, rtok):
    """Tests if an RPAREN token is matched with something other than a plain old
    LPAREN type.
    """
    # note that any([]) is False, so this covers len(lparens) == 0
    return rtok.type == 'RPAREN' and any(x != 'LPAREN' for x in lparens)


def find_next_break(line, mincol=0, lexer=None):
    """Returns the column number of the next logical break in subproc mode.
    This function may be useful in finding the maxcol argument of subproc_toks().
    """
    if mincol >= 1:
        line = line[mincol:]
    if lexer is None:
        lexer = builtins.__tako_execer__.parser.lexer
    if RE_END_TOKS.search(line) is None:
        return None
    maxcol = None
    lparens = []
    lexer.input(line)
    for tok in lexer:
        if tok.type in LPARENS:
            lparens.append(tok.type)
        elif tok.type in END_TOK_TYPES:
            if _is_not_lparen_and_rparen(lparens, tok):
                lparens.pop()
            else:
                maxcol = tok.lexpos + mincol + 1
                break
        elif tok.type == 'ERRORTOKEN' and ')' in tok.value:
            maxcol = tok.lexpos + mincol + 1
            break
    return maxcol


def subproc_toks(line, mincol=-1, maxcol=None, lexer=None, returnline=False):
    """Excapsulates tokens in a source code line in a uncaptured
    subprocess ![] starting at a minimum column. If there are no tokens
    (ie in a comment line) this returns None.
    """
    if lexer is None:
        lexer = builtins.__tako_execer__.parser.lexer
    if maxcol is None:
        maxcol = len(line) + 1
    lexer.reset()
    lexer.input(line)
    toks = []
    lparens = []
    end_offset = 0
    for tok in lexer:
        pos = tok.lexpos
        if tok.type not in END_TOK_TYPES and pos >= maxcol:
            break
        if tok.type in LPARENS:
            lparens.append(tok.type)
        if len(toks) == 0 and tok.type in BEG_TOK_SKIPS:
            continue  # handle indentation
        elif len(toks) > 0 and toks[-1].type in END_TOK_TYPES:
            if _is_not_lparen_and_rparen(lparens, toks[-1]):
                lparens.pop()  # don't continue or break
            elif pos < maxcol and tok.type not in ('NEWLINE', 'DEDENT', 'WS'):
                toks.clear()
                if tok.type in BEG_TOK_SKIPS:
                    continue
            else:
                break
        if pos < mincol:
            continue
        toks.append(tok)
        if tok.type == 'NEWLINE':
            break
        elif tok.type == 'DEDENT':
            # fake a newline when dedenting without a newline
            tok.type = 'NEWLINE'
            tok.value = '\n'
            tok.lineno -= 1
            if len(toks) >= 2:
                prev_tok_end = toks[-2].lexpos + len(toks[-2].value)
            else:
                prev_tok_end = len(line)
            if '#' in line[prev_tok_end:]:
                tok.lexpos = prev_tok_end  # prevents wrapping comments
            else:
                tok.lexpos = len(line)
            break
    else:
        if len(toks) > 0 and toks[-1].type in END_TOK_TYPES:
            if _is_not_lparen_and_rparen(lparens, toks[-1]):
                pass
            else:
                toks.pop()
        if len(toks) == 0:
            return  # handle comment lines
        tok = toks[-1]
        pos = tok.lexpos
        if isinstance(tok.value, str):
            end_offset = len(tok.value.rstrip())
        else:
            el = line[pos:].split('#')[0].rstrip()
            end_offset = len(el)
    if len(toks) == 0:
        return  # handle comment lines
    beg, end = toks[0].lexpos, (toks[-1].lexpos + end_offset)
    end = len(line[:end].rstrip())
    rtn = '?[' + line[beg:end] + ']'
    if returnline:
        rtn = line[:beg] + rtn + line[end:]
    return rtn


def subexpr_from_unbalanced(expr, ltok, rtok):
    """Attempts to pull out a valid subexpression for unbalanced grouping,
    based on opening tokens, eg. '(', and closing tokens, eg. ')'.  This
    does not do full tokenization, but should be good enough for tab
    completion.
    """
    lcnt = expr.count(ltok)
    if lcnt == 0:
        return expr
    rcnt = expr.count(rtok)
    if lcnt == rcnt:
        return expr
    subexpr = expr.rsplit(ltok, 1)[-1]
    subexpr = subexpr.rsplit(',', 1)[-1]
    subexpr = subexpr.rsplit(':', 1)[-1]
    return subexpr


def decode(s, encoding=None):
    encoding = encoding or DEFAULT_ENCODING
    return s.decode(encoding, "replace")


def encode(u, encoding=None):
    encoding = encoding or DEFAULT_ENCODING
    return u.encode(encoding, "replace")


def cast_unicode(s, encoding=None):
    if isinstance(s, bytes):
        return decode(s, encoding)
    return s


def safe_hasattr(obj, attr):
    """In recent versions of Python, hasattr() only catches AttributeError.
    This catches all errors.
    """
    try:
        getattr(obj, attr)
        return True
    except Exception:  # pylint:disable=bare-except
        return False


def indent(instr, nspaces=4, ntabs=0, flatten=False):
    """Indent a string a given number of spaces or tabstops.

    indent(str,nspaces=4,ntabs=0) -> indent str by ntabs+nspaces.

    Parameters
    ----------
    instr : basestring
        The string to be indented.
    nspaces : int (default: 4)
        The number of spaces to be indented.
    ntabs : int (default: 0)
        The number of tabs to be indented.
    flatten : bool (default: False)
        Whether to scrub existing indentation.  If True, all lines will be
        aligned to the same indentation.  If False, existing indentation will
        be strictly increased.

    Returns
    -------
    outstr : string indented by ntabs and nspaces.

    """
    if instr is None:
        return
    ind = '\t' * ntabs + ' ' * nspaces
    if flatten:
        pat = re.compile(r'^\s*', re.MULTILINE)
    else:
        pat = re.compile(r'^', re.MULTILINE)
    outstr = re.sub(pat, ind, instr)
    if outstr.endswith(os.linesep + ind):
        return outstr[:-len(ind)]
    else:
        return outstr


# The following redirect classes were taken directly from Python 3.5's source
# code (from the contextlib module). This can be removed when 3.5 is released,
# although redirect_stdout exists in 3.4, redirect_stderr does not.
# See the Python software license: https://docs.python.org/3/license.html
# Copyright (c) Python Software Foundation. All rights reserved.
class _RedirectStream:

    _stream = None

    def __init__(self, new_target):
        self._new_target = new_target
        # We use a list of old targets to make this CM re-entrant
        self._old_targets = []

    def __enter__(self):
        self._old_targets.append(getattr(sys, self._stream))
        setattr(sys, self._stream, self._new_target)
        return self._new_target

    def __exit__(self, exctype, excinst, exctb):
        setattr(sys, self._stream, self._old_targets.pop())


class redirect_stdout(_RedirectStream):
    """Context manager for temporarily redirecting stdout to another file::

        # How to send help() to stderr
        with redirect_stdout(sys.stderr):
            help(dir)

        # How to write help() to a file
        with open('help.txt', 'w') as f:
            with redirect_stdout(f):
                help(pow)

    Mostly for backwards compatibility.
    """
    _stream = "stdout"


class redirect_stderr(_RedirectStream):
    """Context manager for temporarily redirecting stderr to another file."""
    _stream = "stderr"


def _yield_accessible_unix_file_names(path):
    """yield file names of executable files in path"""
    if not os.path.isdir(path):
        return
    for file_ in scandir(path):
        try:
            if file_.is_file() and os.access(file_.path, os.X_OK):
                yield file_.name
        except (FileNotFoundError, NotADirectoryError):
            # broken Symlink are neither dir not files
            pass


def _executables_in_posix(path):
    if not os.path.exists(path):
        return
    elif PYTHON_VERSION_INFO < (3, 5, 0):
        for fname in os.listdir(path):
            fpath  = os.path.join(path, fname)
            if (os.path.exists(fpath) and os.access(fpath, os.X_OK) and \
                                    (not os.path.isdir(fpath))):
                yield fname
    else:
        yield from _yield_accessible_unix_file_names(path)


def executables_in(path):
    """Returns a generator of files in path that the user could execute. """
    try:
        yield from _executables_in_posix(path)
    except PermissionError:
        return


def command_not_found(cmd):
    """Uses the debian/ubuntu command-not-found utility to suggest packages for a
    command that cannot currently be found.
    """
    if not os.path.isfile('/usr/lib/command-not-found'):
        # utility is not on PATH
        return ''
    c = '/usr/lib/command-not-found {0}; exit 0'
    s = subprocess.check_output(c.format(cmd), universal_newlines=True,
                                stderr=subprocess.STDOUT, shell=True)
    return s.rstrip()


def suggest_commands(cmd, env, aliases):
    """Suggests alternative commands given an environment and aliases."""
    settings = env['TAKO_SETTINGS']
    if not settings.suggest_commands:
        return
    thresh = settings.suggest_threshold
    max_sugg = settings.suggest_max_num
    if max_sugg < 0:
        max_sugg = float('inf')
    cmd = cmd.lower()
    suggested = {}

    for alias in aliases:
        if alias not in suggested:
            if levenshtein(alias.lower(), cmd, thresh) < thresh:
                suggested[alias] = 'Alias'

    for path in filter(os.path.isdir, env.get('PATH')):
        for _file in executables_in(path):
            if _file not in suggested \
                    and levenshtein(_file.lower(), cmd, thresh) < thresh:
                suggested[_file] = 'Command ({0})'.format(os.path.join(path, _file))

    suggested = OrderedDict(
        sorted(suggested.items(),
               key=lambda x: suggestion_sort_helper(x[0].lower(), cmd)))
    num = min(len(suggested), max_sugg)

    if num == 0:
        rtn = command_not_found(cmd)
    else:
        oneof = '' if num == 1 else 'one of '
        tips = 'Did you mean {}the following?'.format(oneof)
        items = list(suggested.popitem(False) for _ in range(num))
        length = max(len(key) for key, _ in items) + 2
        alternatives = '\n'.join('    {: <{}} {}'.format(key + ":", length, val)
                                 for key, val in items)
        rtn = '{}\n{}'.format(tips, alternatives)
        c = command_not_found(cmd)
        rtn += ('\n\n' + c) if len(c) > 0 else ''
    return rtn


def print_exception(msg=None):
    """Print exceptions with/without traceback."""
    env = getattr(builtins, '__tako_env__', None)
    # flags indicating whether the traceback options have been manually set
    if env is None:
        manually_set_trace = False
        manually_set_logfile = False
    else:
        settings = env['TAKO_SETTINGS']
        manually_set_trace = settings.is_manually_set('SHOW_TRACEBACK')
        manually_set_logfile = settings.is_manually_set('TRACEBACK_LOGFILE')
    if (not manually_set_trace) and (not manually_set_logfile):
        # Notify about the traceback output possibility if neither of
        # the two options have been manually set
        sys.stderr.write('tako: For full traceback, set: '
                         '$TAKO_SETTINGS.show_traceback = True\n')
    # get env option for traceback and convert it if necessary
    show_trace = settings.show_traceback
    if not is_bool(show_trace):
        show_trace = to_bool(show_trace)
    # if the trace option has been set, print all traceback info to stderr
    if show_trace:
        # notify user about TAKO_TRACEBACK_LOGFILE if it has
        # not been set manually
        if not manually_set_logfile:
            sys.stderr.write('tako: To log full traceback to a file, set: '
                             '$TAKO_SETTINGS.traceback_logfile = <filename>\n')
        traceback.print_exc()
    # additionally, check if a file for traceback logging has been
    # specified and convert to a proper option if needed
    log_file = settings.traceback_logfile
    log_file = to_logfile_opt(log_file)
    if log_file:
        # if log_file <> '' or log_file <> None, append
        # traceback log there as well
        with open(os.path.abspath(log_file), 'a') as f:
            traceback.print_exc(file=f)

    if not show_trace:
        # if traceback output is disabled, print the exception's
        # error message on stderr.
        display_error_message()
    if msg:
        msg = msg if msg.endswith('\n') else msg + '\n'
        sys.stderr.write(msg)


def display_error_message():
    """
    Prints the error message of the current exception on stderr.
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    exception_only = traceback.format_exception_only(exc_type, exc_value)
    sys.stderr.write(''.join(exception_only))


def is_writable_file(filepath):
    """
    Checks if a filepath is valid for writing.
    """
    # convert to absolute path if needed
    if not os.path.isabs(filepath):
        filepath = os.path.abspath(filepath)
    # cannot write to directories
    if os.path.isdir(filepath):
        return False
    # if the file exists and is writable, we're fine
    if os.path.exists(filepath):
        return True if os.access(filepath, os.W_OK) else False
    # if the path doesn't exist, isolate its directory component
    # and ensure that directory is writable instead
    return os.access(os.path.dirname(filepath), os.W_OK)

# Modified from Public Domain code, by Magnus Lie Hetland
# from http://hetland.org/coding/python/levenshtein.py
def levenshtein(a, b, max_dist=float('inf')):
    """Calculates the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if abs(n - m) > max_dist:
        return float('inf')
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n
    current = range(n + 1)
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change + 1
            current[j] = min(add, delete, change)
    return current[n]


def suggestion_sort_helper(x, y):
    """Returns a score (lower is better) for x based on how similar
    it is to y.  Used to rank suggestions."""
    x = x.lower()
    y = y.lower()
    lendiff = len(x) + len(y)
    inx = len([i for i in x if i not in y])
    iny = len([i for i in y if i not in x])
    return lendiff + inx + iny


def escape_windows_cmd_string(s):
    """Returns a string that is usable by the Windows cmd.exe.
    The escaping is based on details here and emperical testing:
    http://www.robvanderwoude.com/escapechars.php
    """
    for c in '()%!^<>&|"':
        s = s.replace(c, '^' + c)
    s = s.replace('/?', '/.')
    return s


def argvquote(arg, force=False):
    """ Returns an argument quoted in such a way that that CommandLineToArgvW
    on Windows will return the argument string unchanged.
    This is the same thing Popen does when supplied with an list of arguments.
    Arguments in a command line should be separated by spaces; this
    function does not add these spaces. This implementation follows the
    suggestions outlined here:
    https://blogs.msdn.microsoft.com/twistylittlepassagesallalike/2011/04/23/everyone-quotes-command-line-arguments-the-wrong-way/
    """
    if not force and len(arg) != 0 and not any([c in arg for c in ' \t\n\v"']):
        return arg
    else:
        n_backslashes = 0
        cmdline = '"'
        for c in arg:
            if c == '"':
                cmdline += (n_backslashes * 2 + 1) * '\\'
            else:
                cmdline += n_backslashes * '\\'
            if c != '\\':
                cmdline += c
                n_backslashes = 0
            else:
                n_backslashes += 1
        return cmdline + n_backslashes * 2 * '\\' + '"'


#
# Validators and contervers
#


def is_int(x):
    """Tests if something is an integer"""
    return isinstance(x, int)


def is_float(x):
    """Tests if something is a float"""
    return isinstance(x, float)


def is_string(x):
    """Tests if something is a string"""
    return isinstance(x, str)


def is_callable(x):
    """Tests if something is callable"""
    return callable(x)


def is_string_or_callable(x):
    """Tests if something is a string or callable"""
    return is_string(x) or is_callable(x)


def always_true(x):
    """Returns True"""
    return True


def always_false(x):
    """Returns False"""
    return False


def ensure_string(x):
    """Returns a string if x is not a string, and x if it already is."""
    return str(x)


def is_env_path(x):
    """This tests if something is an environment path, ie a list of strings."""
    return isinstance(x, EnvPath)


def str_to_env_path(x):
    """Converts a string to an environment path, ie a list of strings,
    splitting on the OS separator.
    """
    return EnvPath(x)


def env_path_to_str(x):
    """Converts an environment path to a string by joining on the OS separator."""
    return os.pathsep.join(x)


def is_bool(x):
    """Tests if something is a boolean."""
    return isinstance(x, bool)


def is_logfile_opt(x):
    """
    Checks if x is a valid $TAKO_TRACEBACK_LOGFILE option. Returns False
    if x is not a writable/creatable file or an empty string or None.
    """
    if x is None:
        return True
    return False if not isinstance(x, str) else \
           (is_writable_file(x) or x == '')


def to_logfile_opt(x):
    """
    Converts a $TAKO_TRACEBACK_LOGFILE option to either a str containing
    the filepath if it is a writable file or None if the filepath is not
    valid, informing the user on stderr about the invalid choice.
    """
    if is_logfile_opt(x):
        return x
    else:
        # if option is not valid, return a proper
        # option and inform the user on stderr
        sys.stderr.write('tako: $TAKO_SETTINGS.traceback_logfile must be a '
                         'filepath pointing to a file that either exists '
                         'and is writable or that can be created.\n')
        return None


def logfile_opt_to_str(x):
    """
    Detypes a $TAKO_TRACEBACK_LOGFILE option.
    """
    if x is None:
        # None should not be detyped to 'None', as 'None' constitutes
        # a perfectly valid filename and retyping it would introduce
        # ambiguity. Detype to the empty string instead.
        return ''
    return str(x)


_FALSES = frozenset(['', '0', 'n', 'f', 'no', 'none', 'false'])


def to_bool(x):
    """"Converts to a boolean in a semantically meaningful way."""
    if isinstance(x, bool):
        return x
    elif isinstance(x, str):
        return False if x.lower() in _FALSES else True
    else:
        return bool(x)


def bool_to_str(x):
    """Converts a bool to an empty string if False and the string '1' if True."""
    return '1' if x else ''


_BREAKS = frozenset(['b', 'break', 's', 'skip', 'q', 'quit'])


def to_bool_or_break(x):
    if isinstance(x, str) and x.lower() in _BREAKS:
        return 'break'
    else:
        return to_bool(x)


def is_bool_or_int(x):
    """Returns whether a value is a boolean or integer."""
    return is_bool(x) or is_int(x)


def to_bool_or_int(x):
    """Converts a value to a boolean or an integer."""
    if isinstance(x, str):
        return int(x) if x.isdigit() else to_bool(x)
    elif is_int(x):  # bools are ints too!
        return x
    else:
        return bool(x)


def bool_or_int_to_str(x):
    """Converts a boolean or integer to a string."""
    return bool_to_str(x) if is_bool(x) else str(x)


def ensure_int_or_slice(x):
    """Makes sure that x is list-indexable."""
    if x is None:
        return slice(None)
    elif is_int(x):
        return x
    # must have a string from here on
    if ':' in x:
        x = x.strip('[]()')
        return slice(*(int(x) if len(x) > 0 else None for x in x.split(':')))
    else:
        return int(x)


def is_string_set(x):
    """Tests if something is a set of strings"""
    return (isinstance(x, Set) and
            all(isinstance(a, str) for a in x))


def csv_to_set(x):
    """Convert a comma-separated list of strings to a set of strings."""
    if not x:
        return set()
    else:
        return set(x.split(','))


def set_to_csv(x):
    """Convert a set of strings to a comma-separated list of strings."""
    return ','.join(x)


def pathsep_to_set(x):
    """Converts a os.pathsep separated string to a set of strings."""
    if not x:
        return set()
    else:
        return set(x.split(os.pathsep))


def set_to_pathsep(x, sort=False):
    """Converts a set to an os.pathsep separated string. The sort kwarg
    specifies whether to sort the set prior to str conversion.
    """
    if sort:
        x = sorted(x)
    return os.pathsep.join(x)


def is_string_seq(x):
    """Tests if something is a sequence of strings"""
    return (isinstance(x, abc.Sequence) and
            all(isinstance(a, str) for a in x))


def is_nonstring_seq_of_strings(x):
    """Tests if something is a sequence of strings, where the top-level
    sequence is not a string itself.
    """
    return (isinstance(x, abc.Sequence) and not isinstance(x, str) and
            all(isinstance(a, str) for a in x))


def pathsep_to_seq(x):
    """Converts a os.pathsep separated string to a sequence of strings."""
    if not x:
        return []
    else:
        return x.split(os.pathsep)


def seq_to_pathsep(x):
    """Converts a sequence to an os.pathsep separated string."""
    return os.pathsep.join(x)


def pathsep_to_upper_seq(x):
    """Converts a os.pathsep separated string to a sequence of
    uppercase strings.
    """
    if not x:
        return []
    else:
        return x.upper().split(os.pathsep)


def seq_to_upper_pathsep(x):
    """Converts a sequence to an uppercase os.pathsep separated string."""
    return os.pathsep.join(x).upper()


def is_bool_seq(x):
    """Tests if an object is a sequence of bools."""
    return isinstance(x, Sequence) and all(isinstance(y, bool) for y in x)


def csv_to_bool_seq(x):
    """Takes a comma-separated string and converts it into a list of bools."""
    return [to_bool(y) for y in csv_to_set(x)]


def bool_seq_to_csv(x):
    """Converts a sequence of bools to a comma-separated string."""
    return ','.join(map(str, x))


def is_completions_display_value(x):
    return x in {'none', 'single', 'multi'}


def to_completions_display_value(x):
    x = str(x).lower()
    if x in {'none', 'false'}:
        x = 'none'
    elif x in {'multi', 'true'}:
        x = 'multi'
    elif x == 'single':
        pass
    else:
        warn('"{}" is not a valid value for $COMPLETIONS_DISPLAY. '.format(x) +
             'Using "multi".', RuntimeWarning)
        x = 'multi'
    return x


def is_dynamic_cwd_width(x):
    """ Determine if the input is a valid input for the DYNAMIC_CWD_WIDTH
    environement variable.
    """
    return isinstance(x, tuple) and len(x) == 2 and isinstance(x[0], float) and \
           (x[1] in set('c%'))


def to_dynamic_cwd_tuple(x):
    """Convert to a canonical cwd_width tuple."""
    unit = 'c'
    if isinstance(x, str):
        if x[-1] == '%':
            x = x[:-1]
            unit = '%'
        else:
            unit = 'c'
        return (float(x), unit)
    else:
        return (float(x[0]), x[1])


def dynamic_cwd_tuple_to_str(x):
    """Convert a canonical cwd_width tuple to a string."""
    if x[1] == '%':
        return str(x[0]) + '%'
    else:
        return str(x[0])

_RE_STRING_START = "[bBrRuU]*"
_RE_STRING_TRIPLE_DOUBLE = '"""'
_RE_STRING_TRIPLE_SINGLE = "'''"
_RE_STRING_DOUBLE = '"'
_RE_STRING_SINGLE = "'"
_STRINGS = (_RE_STRING_TRIPLE_DOUBLE,
            _RE_STRING_TRIPLE_SINGLE,
            _RE_STRING_DOUBLE,
            _RE_STRING_SINGLE)
RE_BEGIN_STRING = re.compile("(" + _RE_STRING_START +
                             '(' + "|".join(_STRINGS) +
                             '))')
"""Regular expression matching the start of a string, including quotes and
leading characters (r, b, or u)"""

RE_STRING_START = re.compile(_RE_STRING_START)
"""Regular expression matching the characters before the quotes when starting a
string (r, b, or u, case insensitive)"""

RE_STRING_CONT = {k: re.compile(v) for k,v in {
    '"': r'((\\(.|\n))|([^"\\]))*',
    "'": r"((\\(.|\n))|([^'\\]))*",
    '"""': r'((\\(.|\n))|([^"\\])|("(?!""))|\n)*',
    "'''": r"((\\(.|\n))|([^'\\])|('(?!''))|\n)*",
}.items()}
"""Dictionary mapping starting quote sequences to regular expressions that
match the contents of a string beginning with those quotes (not including the
terminating quotes)"""


def check_for_partial_string(x):
    """
    Returns the starting index (inclusive), ending index (exclusive), and
    starting quote string of the most recent Python string found in the input.

    check_for_partial_string(x) -> (startix, endix, quote)

    Parameters
    ----------
    x : str
        The string to be checked (representing a line of terminal input)

    Returns
    -------
    startix : int (or None)
        The index where the most recent Python string found started
        (inclusive), or None if no strings exist in the input

    endix : int (or None)
        The index where the most recent Python string found ended (exclusive),
        or None if no strings exist in the input OR if the input ended in the
        middle of a Python string

    quote : str (or None)
        A string containing the quote used to start the string (e.g., b", ",
        '''), or None if no string was found.
    """
    string_indices = []
    starting_quote = []
    current_index = 0
    match = re.search(RE_BEGIN_STRING, x)
    while match is not None:
        # add the start in
        start = match.start()
        quote = match.group(0)
        lenquote = len(quote)
        current_index += start
        # store the starting index of the string, as well as the
        # characters in the starting quotes (e.g., ", ', """, r", etc)
        string_indices.append(current_index)
        starting_quote.append(quote)
        # determine the string that should terminate this string
        ender = re.sub(RE_STRING_START, '', quote)
        x = x[start + lenquote:]
        current_index += lenquote
        # figure out what is inside the string
        continuer = RE_STRING_CONT[ender]
        contents = re.match(continuer, x)
        inside = contents.group(0)
        leninside = len(inside)
        current_index += contents.start() + leninside + len(ender)
        # if we are not at the end of the input string, add the ending index of
        # the string to string_indices
        if contents.end() < len(x):
            string_indices.append(current_index)
        x = x[leninside + len(ender):]
        # find the next match
        match = re.search(RE_BEGIN_STRING, x)
    numquotes = len(string_indices)
    if numquotes == 0:
        return (None, None, None)
    elif numquotes % 2:
        return (string_indices[-1], None, starting_quote[-1])
    else:
        return (string_indices[-2], string_indices[-1], starting_quote[-1])


# expandvars is a modified version of os.path.expandvars from the Python 3.5.1
# source code (root/Lib/ntpath.py, line 353)

def _is_in_env(name):
    env = builtins.__tako_env__
    return name in env._d or name in env._defaults

def _get_env_string(name):
    env = builtins.__tako_env__
    value = env.get(name)
    ensurer = env.get_ensurer(name)
    if ensurer.detype is bool_to_str:
        value = ensure_string(value)
    else:
        value = ensurer.detype(value)
    return value


def expandvars(path):
    """Expand shell variables of the forms $var, ${var} and %var%.

    Unknown variables are left unchanged."""
    env = builtins.__tako_env__
    settings = env['TAKO_SETTINGS']
    if isinstance(path, bytes):
        path = path.decode(encoding=settings.encoding,
                           errors=settings.encoding_errors)
    elif isinstance(path, pathlib.Path):
        # get the string representation
        path = str(path)
    if '$' not in path:
        return path
    varchars = string.ascii_letters + string.digits + '_-'
    quote = '\''
    brace = '{'
    rbrace = '}'
    dollar = '$'
    res = path[:0]
    index = 0
    pathlen = len(path)
    while index < pathlen:
        c = path[index:index+1]
        if c == quote:   # no expansion within single quotes
            path = path[index + 1:]
            pathlen = len(path)
            try:
                index = path.index(c)
                res += c + path[:index + 1]
            except ValueError:
                res += c + path
                index = pathlen - 1
        elif c == dollar:  # variable or '$$'
            if path[index + 1:index + 2] == dollar:
                res += c
                index += 1
            elif path[index + 1:index + 2] == brace:
                path = path[index+2:]
                pathlen = len(path)
                try:
                    index = path.index(rbrace)
                except ValueError:
                    res += dollar + brace + path
                    index = pathlen - 1
                else:
                    var = path[:index]
                    try:
                        var = eval(var, builtins.__tako_ctx__)
                        if _is_in_env(var):
                            value = _get_env_string(var)
                        elif var is Ellipsis:
                            value = dollar + brace + '...' + rbrace
                        else:
                            value = dollar + brace + var + rbrace
                    except:
                        value = dollar + brace + var + rbrace
                    res += value
            else:
                var = path[:0]
                index += 1
                c = path[index:index + 1]
                while c and c in varchars:
                    var += c
                    index += 1
                    c = path[index:index + 1]
                if _is_in_env(var):
                    value = _get_env_string(var)
                else:
                    value = dollar + var
                res += value
                if c:
                    index -= 1
        else:
            res += c
        index += 1
    return res

#
# File handling tools
#

def backup_file(fname):
    """Moves an existing file to a new name that has the current time right
    before the extension.
    """
    # lazy imports
    import shutil
    from datetime import datetime
    base, ext = os.path.splitext(fname)
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    newfname = '%s.%s%s' % (base, timestamp, ext)
    shutil.move(fname, newfname)


def normabspath(p):
    """Retuns as normalized absolute path, namely, normcase(abspath(p))"""
    return os.path.normcase(os.path.abspath(p))


class CommandsCache(abc.Mapping):
    """A lazy cache representing the commands available on the file system.
    The keys are the command names and the values a tuple of (loc, has_alias)
    where loc is either a str pointing to the executable on the file system or
    None (if no executable exists) and has_alias is a boolean flag for whether
    the command has an alias.
    """

    def __init__(self):
        self._cmds_cache = {}
        self._path_checksum = None
        self._alias_checksum = None
        self._path_mtime = -1

    def __contains__(self, key):
        return key in self.all_commands

    def __iter__(self):
        return iter(self.all_commands)

    def __len__(self):
        return len(self.all_commands)

    def __getitem__(self, key):
        return self.all_commands[key]

    @property
    def all_commands(self):
        paths = builtins.__tako_env__.get('PATH', [])
        pathset = frozenset(x for x in paths if os.path.isdir(x))
        # did PATH change?
        path_hash = hash(pathset)
        cache_valid = path_hash == self._path_checksum
        self._path_checksum = path_hash
        # did aliases change?
        settings = builtins.__tako_env__['TAKO_SETTINGS']
        alss = set(getattr(settings, 'aliases', set()))
        for i in settings.plugins:
            alss |= set(settings.plugins[i].aliases.keys())
        al_hash = hash(frozenset(alss))
        cache_valid = cache_valid and al_hash == self._alias_checksum
        self._alias_checksum = al_hash
        # did the contents of any directory in PATH change?
        max_mtime = 0
        for path in pathset:
            mtime = os.stat(path).st_mtime
            if mtime > max_mtime:
                max_mtime = mtime
        cache_valid = cache_valid and (max_mtime <= self._path_mtime)
        self._path_mtime = max_mtime
        if cache_valid:
            return self._cmds_cache
        allcmds = {}
        for path in reversed(paths):
            # iterate backwards so that enties at the front of PATH overwrite
            # entries at the back (cleverness from @scopatz)
            for cmd in executables_in(path):
                key = cmd
                allcmds[key] = (os.path.join(path, cmd), cmd in alss)
            only_alias = (None, True)
        for cmd in alss:
            if cmd not in allcmds:
                allcmds[cmd] = only_alias
        self._cmds_cache = allcmds
        return allcmds

    def lazyin(self, value):
        """Checks if the value is in the current cache without the potential to
        update the cache. It just says whether the value is known *now*. This
        may not reflect precisely what is on the $PATH.
        """
        return value in self._cmds_cache

    def lazyiter(self):
        """Returns an iterator over the current cache contents without the
        potential to update the cache. This may not reflect what is on the
        $PATH.
        """
        return iter(self._cmds_cache)

    def lazylen(self):
        """Returns the length of the current cache contents without the
        potential to update the cache. This may not reflect precicesly
        what is on the $PATH.
        """
        return len(self._cmds_cache)

    def lazyget(self, key, default=None):
        """A lazy value getter."""
        return self._cmds_cache.get(key, default)


def expand_case_matching(s):
    """Expands a string to a case insenstive globable string."""
    t = []
    openers = {'[', '{'}
    closers = {']', '}'}
    nesting = 0

    drive_part = None

    if drive_part:
        drive_part = drive_part.group(0)
        t.append(drive_part)
        s = s[len(drive_part):]

    for c in s:
        if c in openers:
            nesting += 1
        elif c in closers:
            nesting -= 1
        elif nesting > 0:
            pass
        elif c.isalpha():
            folded = c.casefold()
            if len(folded) == 1:
                c = '[{0}{1}]'.format(c.upper(), c.lower())
            else:
                newc = ['[{0}{1}]?'.format(f.upper(), f.lower())
                        for f in folded[:-1]]
                newc = ''.join(newc)
                newc += '[{0}{1}{2}]'.format(folded[-1].upper(),
                                             folded[-1].lower(),
                                             c)
                c = newc
        t.append(c)
    return ''.join(t)


def globpath(s, ignore_case=False, return_empty=False):
    """Simple wrapper around glob that also expands home and env vars."""
    o, s = _iglobpath(s, ignore_case=ignore_case)
    o = list(o)
    no_match = [] if return_empty else [s]
    return list(sorted(o)) if len(o) != 0 else no_match


def _iglobpath(s, ignore_case=False):
    s = builtins.__tako_expand_path__(s)
    if ignore_case:
        s = expand_case_matching(s)
    if sys.version_info > (3, 5):
        if '**' in s and '**/*' not in s:
            s = s.replace('**', '**/*')
        # `recursive` is only a 3.5+ kwarg.
        return iglob(s, recursive=True), s
    else:
        return iglob(s), s

def iglobpath(s, ignore_case=False):
    """Simple wrapper around iglob that also expands home and env vars."""
    return list(sorted(_iglobpath(s, ignore_case)[0]))

COLORS_TAKO = {
    # Reset
    'NO_COLOR': '\001\033[0m\002',  # Text Reset
    # Regular Colors
    'BLACK': '\001\033[0;30m\002',  # BLACK
    'RED': '\001\033[0;31m\002',  # RED
    'GREEN': '\001\033[0;32m\002',  # GREEN
    'YELLOW': '\001\033[0;33m\002',  # YELLOW
    'BLUE': '\001\033[0;34m\002',  # BLUE
    'PURPLE': '\001\033[0;35m\002',  # PURPLE
    'CYAN': '\001\033[0;36m\002',  # CYAN
    'WHITE': '\001\033[0;37m\002',  # WHITE
    # Bold
    'BOLD_BLACK': '\001\033[1;30m\002',  # BLACK
    'BOLD_RED': '\001\033[1;31m\002',  # RED
    'BOLD_GREEN': '\001\033[1;32m\002',  # GREEN
    'BOLD_YELLOW': '\001\033[1;33m\002',  # YELLOW
    'BOLD_BLUE': '\001\033[1;34m\002',  # BLUE
    'BOLD_PURPLE': '\001\033[1;35m\002',  # PURPLE
    'BOLD_CYAN': '\001\033[1;36m\002',  # CYAN
    'BOLD_WHITE': '\001\033[1;37m\002',  # WHITE
    # Underline
    'UNDERLINE_BLACK': '\001\033[4;30m\002',  # BLACK
    'UNDERLINE_RED': '\001\033[4;31m\002',  # RED
    'UNDERLINE_GREEN': '\001\033[4;32m\002',  # GREEN
    'UNDERLINE_YELLOW': '\001\033[4;33m\002',  # YELLOW
    'UNDERLINE_BLUE': '\001\033[4;34m\002',  # BLUE
    'UNDERLINE_PURPLE': '\001\033[4;35m\002',  # PURPLE
    'UNDERLINE_CYAN': '\001\033[4;36m\002',  # CYAN
    'UNDERLINE_WHITE': '\001\033[4;37m\002',  # WHITE
    # Background
    'BACKGROUND_BLACK': '\001\033[40m\002',  # BLACK
    'BACKGROUND_RED': '\001\033[41m\002',  # RED
    'BACKGROUND_GREEN': '\001\033[42m\002',  # GREEN
    'BACKGROUND_YELLOW': '\001\033[43m\002',  # YELLOW
    'BACKGROUND_BLUE': '\001\033[44m\002',  # BLUE
    'BACKGROUND_PURPLE': '\001\033[45m\002',  # PURPLE
    'BACKGROUND_CYAN': '\001\033[46m\002',  # CYAN
    'BACKGROUND_WHITE': '\001\033[47m\002',  # WHITE
    # High Intensity
    'INTENSE_BLACK': '\001\033[0;90m\002',  # BLACK
    'INTENSE_RED': '\001\033[0;91m\002',  # RED
    'INTENSE_GREEN': '\001\033[0;92m\002',  # GREEN
    'INTENSE_YELLOW': '\001\033[0;93m\002',  # YELLOW
    'INTENSE_BLUE': '\001\033[0;94m\002',  # BLUE
    'INTENSE_PURPLE': '\001\033[0;95m\002',  # PURPLE
    'INTENSE_CYAN': '\001\033[0;96m\002',  # CYAN
    'INTENSE_WHITE': '\001\033[0;97m\002',  # WHITE
    # Bold High Intensity
    'BOLD_INTENSE_BLACK': '\001\033[1;90m\002',  # BLACK
    'BOLD_INTENSE_RED': '\001\033[1;91m\002',  # RED
    'BOLD_INTENSE_GREEN': '\001\033[1;92m\002',  # GREEN
    'BOLD_INTENSE_YELLOW': '\001\033[1;93m\002',  # YELLOW
    'BOLD_INTENSE_BLUE': '\001\033[1;94m\002',  # BLUE
    'BOLD_INTENSE_PURPLE': '\001\033[1;95m\002',  # PURPLE
    'BOLD_INTENSE_CYAN': '\001\033[1;96m\002',  # CYAN
    'BOLD_INTENSE_WHITE': '\001\033[1;97m\002',  # WHITE
    # High Intensity backgrounds
    'BACKGROUND_INTENSE_BLACK': '\001\033[0;100m\002',  # BLACK
    'BACKGROUND_INTENSE_RED': '\001\033[0;101m\002',  # RED
    'BACKGROUND_INTENSE_GREEN': '\001\033[0;102m\002',  # GREEN
    'BACKGROUND_INTENSE_YELLOW': '\001\033[0;103m\002',  # YELLOW
    'BACKGROUND_INTENSE_BLUE': '\001\033[0;104m\002',  # BLUE
    'BACKGROUND_INTENSE_PURPLE': '\001\033[0;105m\002',  # PURPLE
    'BACKGROUND_INTENSE_CYAN': '\001\033[0;106m\002',  # CYAN
    'BACKGROUND_INTENSE_WHITE': '\001\033[0;107m\002',  # WHITE
}

COLORS_256 = {'COLOR_{}'.format(code): '\x1b[38;5;{}m'.format(code) for code in range(256)}
COLORS_256['NO_COLOR'] = '\x1b[0m'
COLORS_256.update(COLORS_TAKO)
