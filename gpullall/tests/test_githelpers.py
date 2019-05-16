import os
import unittest
import sys
sys.path.append("..")
import githelpers  # noqa: E402


class TestGitHelpers(unittest.TestCase):
    def test_get_path(self):
        self.assertIn(
            os.path.abspath("../../"),
            githelpers.get_repositories("../../../"))


if __name__ == "__main__":
    unittest.main()
