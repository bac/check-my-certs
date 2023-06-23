"""Main module."""

from datetime import datetime, timedelta
from urllib.request import ssl, socket

__ALL__ = ("check",)

DATE_FORMAT = "%b %d %H:%M:%S %Y %Z"


def parse_file(fn):
    """Parse the file. Return a list of sites."""
    with open(fn) as fd:
        for line in fd.readlines():
            line = line.strip()
            if ":" not in line:
                host = line
                port = 443
            else:
                host, port = line.split(":")
                port = int(port)

            yield host, port


def parse_date(date_str):
    """Parse the date string and return date object."""
    return datetime.strptime(date_str, DATE_FORMAT)


def check_cert(host, port, warning_date):
    """Check the certificate for the URL."""
    context = ssl.create_default_context()
    try:
        with socket.create_connection((host, port), timeout=1) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssl_sock:
                cert = ssl_sock.getpeercert()
                not_before = parse_date(cert["notBefore"])
                not_after = parse_date(cert["notAfter"])
                if not_after < warning_date or not_before > datetime.now():
                    flag = "❌"
                else:
                    flag = "✅"
    except TimeoutError:
        flag = "❌⏰"
        not_after = "N/A"

    print_result(f"{host}:{port}", str(not_after), flag)


def print_result(url, expiry, flag):
    """Display the result."""
    line = f"{url:25s} {expiry:20s} {flag}"
    print(line)


def check(fn, days):
    """Run the certificate checker."""
    warning_date = datetime.now() + timedelta(days=days)
    for host, port in parse_file(fn):
        check_cert(host, port, warning_date)
