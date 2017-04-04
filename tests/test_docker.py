import os
import unittest

import buildhammer.docker as d

DIR = 'tests/sample/docker'

class GitTestCase(unittest.TestCase):

    def test_wrap_command(self):

        image = d.build_image(DIR)

        rc, stdout, stderr = d.wrap_command(image, os.getcwd(), 'true')
        self.assertEqual(rc, 0)

        rc, stdout, stderr = d.wrap_command(image, os.getcwd(), 'false')
        self.assertEqual(rc, 1)
