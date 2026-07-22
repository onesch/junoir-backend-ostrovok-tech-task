import sys
from datetime import datetime

from logger import logger


def parse_arguments() -> tuple[int, int, str]:
    """
    Parses command line arguments: `MMYYYY` `resolution`;

    - Returns a tuple containing a year, month, and resolution string.
    """
    if len(sys.argv) != 3:
        logger.error("Invalid arguments, Usage: ./getwallpapers.py MMYYYY resolution")
        sys.exit(1)

    month_year = sys.argv[1]
    resolution = sys.argv[2]

    if len(month_year) != 6 or not month_year.isdigit():
        raise ValueError(
            "Date must be in MMYYYY format."
        )

    month = int(month_year[:2])
    year = int(month_year[2:])

    validate_arguments(
        year,
        month,
        resolution,
    )

    return year, month, resolution


def validate_arguments(year: int, month: int, resolution: str) -> None:
    if not 1 <= month <= 12:
        raise ValueError(
            "Month must be between 1 and 12."
        )

    now = datetime.now()

    current_year = now.year
    current_month = now.month

    if not 2008 <= year <= current_year:
        raise ValueError(
            f"Year must be between 2008 and {current_year}."
        )

    if (
        year == current_year
        and month > current_month
    ):
        raise ValueError(
            "Cannot request wallpapers from the future."
        )

    parts: list[str] = resolution.split("x")

    if len(parts) != 2:
        raise ValueError(
            "Resolution must be in WIDTHxHEIGHT format."
        )

    width, height = parts

    if not (
        width.isdigit()
        and height.isdigit()
    ):
        raise ValueError(
            "Resolution must contain only numbers."
        )
