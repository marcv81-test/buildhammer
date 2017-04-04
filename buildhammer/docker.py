import os
import re

import buildhammer.process as p

def build_image(dir):
    """Builds a Docker image."""

    command = 'docker build -q ' + dir
    rc, stdout, stderr = p.wrap_command(command)
    if rc != 0:
        message = p.error_message(
            'Could not build Docker image', rc, stdout, stderr)
        raise Exception(message)

    regex = re.compile('^sha256:([0-9a-f]{64})$')
    matches = regex.search(stdout)
    if matches is None:
        message = p.error_message(
            'Could not retrieve Docker image ID', rc, stdout, stderr)
        raise Exception(message)

    image = matches.group(1)
    return image

def wrap_command(image, dir, command):
    """Runs a command in a Docker container."""

    options = ' '.join([
        '--rm',
        '--user ' + str(os.getuid()) + ':' + str(os.getgid()),
        '--volume ' + dir + ':/home/buildhammer',
        '--workdir=/home/buildhammer'])
    command = 'docker run ' + options + ' ' + image + ' ' + command
    return p.wrap_command(command)
