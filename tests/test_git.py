import os
import unittest

import buildhammer.git as git

DIR = os.path.join(os.getcwd(), 'test-workspace')
REPO_URL = 'https://github.com/marcv81/SkiingInSingapore.git'

class GitTestCase(unittest.TestCase):

    def test_checkout(self):

        # Latest master
        with git.Workspace(DIR) as workspace:
            workspace.init(REPO_URL)
            workspace.checkout('refs/heads/master')
            self.assertTrue(os.path.isfile(os.path.join(workspace.dir, 'pom.xml')))

        # Latest master, explicit SHA
        with git.Workspace(DIR) as workspace:
            workspace.init(REPO_URL)
            workspace.checkout('refs/heads/master', revision='28d9072f')
            self.assertTrue(os.path.isfile(os.path.join(workspace.dir, 'pom.xml')))

        # Previous master, explicit SHA (not shallow)
        with git.Workspace(DIR) as workspace:
            workspace.init(REPO_URL)
            workspace.checkout('refs/heads/master', depth=None, revision='74d696b7')
            self.assertTrue(os.path.isfile(os.path.join(workspace.dir, 'pom.xml')))

        # Previous master, explicit SHA (shallow, deep enough)
        with git.Workspace(DIR) as workspace:
            workspace.init(REPO_URL)
            workspace.checkout('refs/heads/master', depth=50, revision='74d696b7')
            self.assertTrue(os.path.isfile(os.path.join(workspace.dir, 'pom.xml')))

        # Previous master, explicit SHA (shallow, not deep enough)
        with git.Workspace(DIR) as workspace:
            with self.assertRaises(Exception) as context:
                workspace.init(REPO_URL)
                workspace.checkout('refs/heads/master', revision='74d696b7')

    def test_execute(self):

       with git.Workspace(DIR) as workspace:
            workspace.init(REPO_URL)
            workspace.checkout('refs/heads/master')
            rc, stdout, stderr = workspace.execute('/usr/bin/mvn compile')
            self.assertEqual(rc, 0)
