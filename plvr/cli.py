
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

import sys

def error(msg, status=1):
    sys.stderr.write('ERROR: ' + msg + '\n')
    sys.exit(status)


def get_answer(msg):
    print msg,
    return sys.stdin.readline().strip()


def get_option(prefix, options, default=None):
    short_to_long = {}
    for long_opt in options:
        for c in long_opt:
            if c not in short_to_long:
                if long_opt == default:
                    c = c.upper()
                short_to_long[c] = long_opt
                break

    short_options = short_to_long.keys()
    short_options.sort()
    answer = get_answer(prefix +
                        ', '.join(["%s(%s)" % (s, short_to_long[s])
                                   for s in short_options]) +
                        ': ')
    if not answer:
        return default
    return short_to_long[answer] if answer in short_to_long else answer
