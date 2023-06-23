#!/usr/bin/env python

"""Tests for `check_my_certs` package."""


import unittest
from click.testing import CliRunner

from check_my_certs import check_my_certs
from check_my_certs import cli


class TestCheck_my_certs(unittest.TestCase):
    """Tests for `check_my_certs` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_parse_file(self):
        """Test parse_file returns an expected list."""
        res = list(check_my_certs.parse_file("tests/files/sites.txt"))
        self.assertEqual(2, len(res))
        self.assertEqual(("google.com", 443), res[0])
        self.assertEqual(("yahoo.com", 8443), res[1])

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        help_result = runner.invoke(cli.main, ["--help"])
        self.assertEqual(0, help_result.exit_code)
        self.assertRegex(help_result.output, r"--help\s+Show this message and exit")
        # result = runner.invoke(cli.main)
        # assert result.exit_code == 0
        # assert "check_my_certs.cli.main" in result.output
