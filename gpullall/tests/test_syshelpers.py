import os
import unittest
import sys
sys.path.append("..")
import syshelpers  # noqa: E402
import settings  # noqa: E402


class TestSysHelpers(unittest.TestCase):
    def test_read_path(self):
        settings.dir_exists = True
        settings.path = os.getcwd()
        output = syshelpers.read_path()
        self.assertEqual(output, os.getcwd())


if __name__ == "__main__":
    unittest.main()
