import unittest
import subprocess

from shopping_list import version

expected_version_string = (subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'])).strip().decode('utf-8')


class TestVersion(unittest.TestCase):

    def test_version_string(self):
        self.assertEqual(expected_version_string, version.version_string)

# TODO add some more tests in here.
