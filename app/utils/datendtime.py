import datetime
import re

from dateutil.parser import parse

from app import Settings
from app.loggs import logger


def parse_datetime(input_string: str) -> datetime.datetime:
    logger.debug(f"Parsing datetime from {input_string}")
    # Parse the input string using a regular expression to extract the relevant information
    m = re.match(r"(?:(\d+y)?(\d+M)?(\d+w)?(\d+d)?(\d+h)?(\d+m)?(\d+s)?)", input_string)  # noqa

    if m and any(item is not None for item in m.groups()):
        logger.debug(f"Matched {m.groups()}")
        years = int(m.group(1).rstrip("y")) if m.group(1) else 0
        months = int(m.group(2).rstrip("M")) if m.group(2) else 0
        weeks = int(m.group(3).rstrip("w")) if m.group(3) else 0
        days = int(m.group(4).rstrip("d")) if m.group(4) else 0
        hours = int(m.group(5).rstrip("h")) if m.group(5) else 0
        minutes = int(m.group(6).rstrip("m")) if m.group(6) else 0
        seconds = int(m.group(7).rstrip("s")) if m.group(7) else 0

        delta = datetime.timedelta(
            weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds
        )
        target_datetime = datetime.datetime.now(tz=Settings.TIMEZONE) + delta
        if years or months:
            from dateutil.relativedelta import relativedelta

            target_datetime = target_datetime + relativedelta(years=years, months=months)

    elif input_string == "tomorrow":
        logger.debug("Matched 'tomorrow'")
        target_datetime = datetime.datetime.now(tz=Settings.TIMEZONE) + datetime.timedelta(days=1)
    elif input_string == "next week":
        logger.debug("Matched 'next week'")
        target_datetime = datetime.datetime.now(tz=Settings.TIMEZONE) + datetime.timedelta(weeks=1)
    else:
        logger.debug("Matched 'parse'")
        # If the input string is not in the expected format, try parsing it using the
        # dateutil.parser module
        target_datetime = parse(input_string)

    logger.debug(f"Returning {target_datetime}")

    return target_datetime
