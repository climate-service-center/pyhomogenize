"""Console script for netcdf_time_control."""
import argparse
import sys

from .pyhomogenize import pyhomogenize


def csv_list(string):
    return string.split(",")


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "operator",
        nargs="?",
        default=None,
        help="Operator",
        type=csv_list,
    ),
    parser.add_argument(
        "-i",
        "--input_files",
        dest="input_files",
        nargs="+",
        help="List of input files",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        dest="output_file",
        help="Name of the putput file",
    )
    parser.add_argument(
        "-ops",
        "--operators",
        dest="operators",
        action="store_true",
        help="Choose to get a list of all available operators.",
    )
    return parser


def main():
    """Console script for netcdf_time_control."""
    parser = create_parser()
    args = parser.parse_args()
    pyhomogenize(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
