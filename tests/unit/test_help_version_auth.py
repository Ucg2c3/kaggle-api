# coding=utf-8
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, "../../src")

from kaggle.api.kaggle_api_extended import KaggleApi


class TestHelpOrVersionAuth(unittest.TestCase):
    """Tests for help/version detection used during authenticate()."""

    def setUp(self):
        self.api = KaggleApi.__new__(KaggleApi)

    def _assert_help_or_version(self, argv, expected):
        with patch.object(sys, "argv", argv):
            api_command = " ".join(argv[1:])
            self.assertEqual(self.api._is_help_or_version_command(api_command), expected)

    def test_top_level_version_and_help(self):
        self._assert_help_or_version(["kaggle", "-v"], True)
        self._assert_help_or_version(["kaggle", "--version"], True)
        self._assert_help_or_version(["kaggle", "-h"], True)
        self._assert_help_or_version(["kaggle", "--help"], True)

    def test_subcommand_csv_flag_is_not_version(self):
        self._assert_help_or_version(["kaggle", "quota", "-v"], False)
        self._assert_help_or_version(["kaggle", "datasets", "list", "-v"], False)

    def test_subcommand_help_still_skips_auth(self):
        self._assert_help_or_version(["kaggle", "quota", "-h"], True)
        self._assert_help_or_version(["kaggle", "datasets", "list", "--help"], True)

    def test_quota_csv_flag_does_not_allow_logged_out(self):
        with patch.object(sys, "argv", ["kaggle", "quota", "-v"]):
            self.assertFalse(self.api._command_allows_logged_out("quota -v"))


if __name__ == "__main__":
    unittest.main()
