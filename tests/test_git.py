import os
import unittest

import buildhammer.git as git

DIR = os.path.join(os.getcwd(), 'test-workspace')
REPO_URL = 'https://github.com/kohsuke/hello-world-webapp'

class GitTestCase(unittest.TestCase):

    def test_checkout(self):

        with git.Workspace(DIR) as workspace:
            workspace.init(REPO_URL)
            workspace.checkout('refs/heads/master')
            self.assertTrue(os.path.isfile(os.path.join(workspace.dir, 'pom.xml')))

    def test_execute(self):

       with git.Workspace(DIR) as workspace:
            workspace.init(REPO_URL)
            workspace.checkout('refs/heads/master')
            rc, stdout, stderr = workspace.execute('/usr/bin/mvn install')
            self.assertEqual(rc, 0)
