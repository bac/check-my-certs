#!/usr/bin/env python

"""Tests for `check_my_certs` package."""


from datetime import datetime, timedelta, timezone
from unittest import mock, TestCase


from click.testing import CliRunner

from check_my_certs import check_my_certs, cli


class TestCheck_my_certs(TestCase):
    """Tests for `check_my_certs` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        help_result = runner.invoke(cli.main, ["--help"])
        self.assertEqual(0, help_result.exit_code)
        help_output = help_result.output
        self.assertRegex(help_output, r"--help\s+Show this message and exit")
        self.assertRegex(
            help_output,
            r"-f, --filename TEXT\s+File listing sites to check.  "
            r"\[default: sites.txt\]",
        )
        self.assertRegex(
            help_output,
            r"-d, --days INTEGER\s+Days until expiry for warning.  \[default: 14\]",
        )

    def test_parse_file(self):
        """Test parse_file returns an expected list."""
        res = list(check_my_certs.parse_file("tests/files/sites.txt"))
        self.assertEqual(2, len(res))
        self.assertEqual(("google.com", 443), res[0])
        self.assertEqual(("yahoo.com", 8443), res[1])

    def test_parse_date(self):
        """Test the parse_date function returns the proper datetime object."""
        testdate = datetime(2023, 5, 1, tzinfo=timezone.utc)
        parsed = check_my_certs.parse_date(
            testdate.strftime(check_my_certs.DATE_FORMAT)
        )
        self.assertEqual(testdate, parsed)

    def test_check_cert(self):
        """Test the cert characterization with all socket interaction mocked out."""
        create_def_ctx = "check_my_certs.check_my_certs.ssl.create_default_context"
        create_conn = "check_my_certs.check_my_certs.socket.create_connection"

        with mock.patch(create_def_ctx) as mock_ctx:
            with mock.patch(create_conn):
                return_value = dict(
                    notBefore=(
                        datetime.now(tz=timezone.utc) - timedelta(days=7)
                    ).strftime(check_my_certs.DATE_FORMAT),
                    notAfter=(
                        datetime.now(tz=timezone.utc) + timedelta(days=30)
                    ).strftime(check_my_certs.DATE_FORMAT),
                )

                with mock_ctx().wrap_socket() as mock_ssl_sock:
                    mock_ssl_sock.getpeercert.return_value = return_value
                    not_after, flag = check_my_certs.check_cert(
                        "example.com", 443, datetime.now(tz=timezone.utc)
                    )
        self.assertEqual("✅", flag)
        self.assertEqual(check_my_certs.parse_date(return_value["notAfter"]), not_after)
