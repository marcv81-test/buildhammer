import os
import re

import buildhammer.process as p

class Workspace:

    def __init__(self, dir):
        self.dir = dir

    def __enter__(self):
        self.create()
        return self

    def __exit__(self, *args):
        self.destroy()
        return False

    def create(self):
        """Creates a workspace."""

        command = 'mkdir ' + self.dir
        rc, stdout, stderr = p.wrap_command(command)
        if rc != 0:
            message = p.error_message(
                'Could not create Git workspace', rc, stdout, stderr)
            raise Exception(message)

    def destroy(self):
        """Destroys a workspace."""

        command = 'rm -rf ' + self.dir
        rc, stdout, stderr = p.wrap_command(command)
        if rc != 0:
            message = p.error_message(
                'Could not destroy Git workspace', rc, stdout, stderr)
            raise Exception(message)

    def init(self, repo_url):
        """Initializes a workspace and adds an origin remote."""

        command = 'git init'
        rc, stdout, stderr = p.wrap_command(command, self.dir)
        if rc != 0:
            message = p.error_message(
                'Could not initialize Git repo', rc, stdout, stderr)
            raise Exception(message)

        command = 'git remote add origin ' + repo_url
        rc, stdout, stderr = p.wrap_command(command, self.dir)
        if rc != 0:
            message = p.error_message(
                'Could not add Git remote', rc, stdout, stderr)
            raise Exception(message)

    def checkout(self, reference, depth=1, revision='FETCH_HEAD'):
        """Fetches and checks out a reference from origin.
        Can check out a parent revision up to a specified depth."""

        command = 'git fetch origin ' + reference
        if depth is not None:
            command += ' --depth ' + str(depth)
        rc, stdout, stderr = p.wrap_command(command, self.dir)
        if rc != 0:
            message = p.error_message(
                'Could fetch Git reference', rc, stdout, stderr)
            raise Exception(message)

        command = 'git checkout ' + revision
        rc, stdout, stderr = p.wrap_command(command, self.dir)
        if rc != 0:
            message = p.error_message(
                'Could not checkout Git reference', rc, stdout, stderr)
            raise Exception(message)

    def execute(self, command):
        """Executes a command in a workspace.
        Returns the exit code, stdout, and stderr."""

        return p.wrap_command(command, self.dir)
