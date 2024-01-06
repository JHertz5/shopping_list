import unittest
import subprocess

from shopping_list import version


class TestVersion(unittest.TestCase):

    def test_version_string(self):
        expected_string = (subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'])).strip().decode('utf-8')
        self.assertEqual(expected_string, version.version_string)
