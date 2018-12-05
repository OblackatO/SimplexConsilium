"""
Created on 25th October 2018 by
blackat.
"""

from enum import Enum, unique


@unique
class DateFormat(Enum):
    """
    Three different date formats.
    """
    BigEndian = 0  # (year, month, day), e.g. 2018-05-27
    LittleEndian = 1  # (day, month, year), e.g. 27-05-2018
    MiddleEndian = 2  # (month, day, year), e.g. 05-27-2018
