from enum import StrEnum, unique


@unique
class Period(StrEnum):
    DAY = 'DAY'
    MONTH = 'MONTH'
    YEAR = 'YEAR'
