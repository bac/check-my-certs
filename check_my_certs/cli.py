"""Console script for check_my_certs."""
import sys
import click
from .check_my_certs import check


@click.command()
@click.option(
    "-f",
    "--filename",
    default="sites.txt",
    help="File listing sites to check.",
    show_default=True,
)
@click.option(
    "-d",
    "--days",
    default=14,
    help="Days until expiry for warning.",
    show_default=True,
)
def main(filename, days):
    """Console script for check_my_certs."""
    check(filename, days)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
