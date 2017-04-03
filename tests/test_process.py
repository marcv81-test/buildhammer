import unittest

import buildhammer.process as p

class ProcessTestCase(unittest.TestCase):

    def test_return_code(self):

        # "/bin/true" returns 0
        rc, stdout, stderr = p.wrap_command('/bin/true')
        self.assertEqual(0, rc)

        # "/bin/false" returns 1
        rc, stdout, stderr = p.wrap_command('/bin/false')
        self.assertEqual(1, rc)

    def test_stdout_stderr(self):

        # "echo hyvä" writes "hyvä" to stdout (and nothing to stderr)
        rc, stdout, stderr = p.wrap_command('/bin/sh -c "echo hyvä"')
        self.assertEqual('hyvä\n', stdout)
        self.assertEqual('', stderr)

        # ">&2 echo hyvä" writes "hyvä" to stderr (and nothing to stdout)
        rc, stdout, stderr = p.wrap_command('/bin/sh -c ">&2 echo hyvä"')
        self.assertEqual('', stdout)
        self.assertEqual('hyvä\n', stderr)
