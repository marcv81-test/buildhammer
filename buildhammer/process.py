import fcntl
import io
import os
import select
import shlex
import subprocess

class Process:
    """Runs commands and captures stdout/stderr efficiently."""

    def __init__(self, on_stdout, on_stderr):
        """Constructor."""

        self.on_stdout = on_stdout
        self.on_stderr = on_stderr

    def run(self, command):
        """Runs a command."""

        process = subprocess.Popen(
            shlex.split(command), shell=False,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout_fd = process.stdout.fileno()
        stderr_fd = process.stderr.fileno()

        # Configure stdout and stderr for non-blocking reads
        def configure_fd(fd):
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        configure_fd(stdout_fd)
        configure_fd(stderr_fd)

        # Wait until stdout and/or stderr is available for reading.
        # An empty read on an available stream indicates its end.
        # Repeat until both streams end.
        read_fds = [stdout_fd, stderr_fd]
        while len(read_fds) > 0:
            fds = select.select(read_fds, [], [])
            for fd in fds[0]:

                # stdout is available for reading
                if fd == stdout_fd:
                    raw_data = process.stdout.read()
                    data = raw_data.decode('utf-8', 'ignore')
                    if len(data) > 0:
                        self.on_stdout(data)
                    else:
                        read_fds.remove(stdout_fd)
                        process.stdout.close()

                # stderr is available for reading
                if fd == stderr_fd:
                    raw_data = process.stderr.read()
                    data = raw_data.decode('utf-8', 'ignore')
                    if len(data) > 0:
                        self.on_stderr(data)
                    else:
                        read_fds.remove(stderr_fd)
                        process.stderr.close()

        process.wait()
        return process.poll()

def wrap_command(command, dir=None):
    """Runs a command. Returns the exit code and stdout/stderr."""

    stdout = io.StringIO()
    stderr = io.StringIO()

    process = Process(
        on_stdout=lambda data: stdout.write(data),
        on_stderr=lambda data: stderr.write(data))

    if dir is not None:
        dir_backup = os.getcwd()
        os.chdir(dir)
    rc = process.run(command)
    if dir is not None:
        os.chdir(dir_backup)

    return rc, stdout.getvalue(), stderr.getvalue()

def error_message(message, rc=None, stdout=None, stderr=None):
    """Formats a process error message."""

    if rc is not None:
        message += '\n## return code: ' + str(rc)

    if stdout is not None:
        message += '\n## stdout:'
        stdout = stdout.strip()
        if len(stdout) > 0:
            message += '\n' + stdout

    if stderr is not None:
        message += '\n## stderr:'
        stderr = stderr.strip()
        if len(stderr) > 0:
            message += '\n' + stderr

    return message
