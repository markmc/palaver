
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

import json

from plvr import git

LOG_ARGS = ['--no-merges', '--topo-order']


def iter_notes(git_range, state=None):
    """Iterate over the notes for commits in a given range."""
    (output, err, code) = git.run_cmd('log', '--oneline', '--reverse',
                                      *(LOG_ARGS + [git_range]))
    if code:
        raise git.GitError('"git log" failed: %s' % err)

    commits = [Commit.parse_oneline(l) for l in output.split('\n') if l]
    for commit in commits:
        note = commit.get_note()
        if state:
            states = note.states_by_author().values()
            if state == "none" and states:
                continue
            elif state != "none" and state not in states:
                continue

        yield note


class Comment(object):

    VERSION = 1  # increment this if you make an incompatible change

    STATES = ['pass', 'defer', 'pick', 'proposed', 'merged']

    class ParseError(Exception):
        pass

    def __init__(self, author, state, message):
        self.version = self.VERSION
        self.author = author
        self.state = state
        self.message = message

    def to_json(self):
        return json.dumps(vars(self))

    @classmethod
    def parse(cls, js):
        """Create a Comment object from a json string."""
        c = json.loads(js)
        if c['version'] != cls.VERSION:
            raise cls.ParseError('Unknown json version "%s"' % c['version'])
        return cls(c['author'], c['state'], c['message'])


class Note(object):

    def __init__(self, commit, comments):
        self.commit = commit
        self.comments = comments

    def states_by_author(self):
        """Return a mapping of author to latest state."""
        ret = {}
        for comment in self.comments:
            if comment.state:
                ret[comment.author] = comment.state
        return ret

    @classmethod
    def parse(cls, commit, lines):
        """Parse a json comments for a commit, one comment per line."""
        return cls(commit, [Comment.parse(l) for l in lines if l])


class Commit(object):

    def __init__(self, id, shortlog):
        self.id = id
        self.shortlog = shortlog

    def get_note(self):
        """Return the Note associated with this commit,"""
        (output, err, code) = git.run_cmd('notes', 'show', self.id)
        return Note.parse(self, output.split('\n') if not code else [])

    def add_comment(self, author, state, message):
        """Add a comment to a commit note."""
        comment = Comment(author, state, message)

        (output, err, code) = git.run_cmd('notes', 'append', '--file=-',
                                          self.id, stdin=comment.to_json())
        if code:
            raise git.GitError('"git notes append" failed: %s' % err)

    @classmethod
    def parse_oneline(cls, line):
        """Parse a line of 'git log --oneline' output."""
        return cls(*line.split(' ', 1))

    @classmethod
    def get(cls, id):
        """Get a Commit object for a given commit id."""
        (output, err, code) = git.run_cmd('log', '--oneline', '-1', id)
        if code:
            raise git.GitError('"git log" failed: %s' % err)
        return cls.parse_oneline(output.strip())
