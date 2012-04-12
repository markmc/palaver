
#
# Copyright 2012 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

import os
import subprocess


class GitError(Exception):
    pass


def run_cmd(cmd, *args, **kwargs):
    """Run a git command.

    :param cmd: git command name e.g. 'commit'
    :param args: the argument list e.g. ['-m', 'foo']
    :param stdin: a string to pass via stdin
    :param cwd: the directory to run from
    :param kwargs: environment variables to set
    :returns: tuple with stdout, stderr and exit status
    """
    stdin = kwargs.pop('stdin', None)
    cwd = kwargs.pop('cwd', None)
    if kwargs:
        env = os.environ.copy()
        env.update(kwargs)
    else:
        env = None
    p = subprocess.Popen(['git', cmd] + list(args),
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         cwd=cwd,
                         env=env)
    (stdout, stderr) = p.communicate(stdin)
    return (stdout, stderr, p.returncode)


def whoami():
    def git_config(name):
        (output, err, code) = run_cmd('config', name)
        if code:
            raise GitError('Failed to run "git config": ' + err)
        return output.strip()
    return git_config('user.email')
