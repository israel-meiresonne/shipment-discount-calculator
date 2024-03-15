from enum import StrEnum, unique


@unique
class Provider(StrEnum):
    LP = 'LP'
    MR = 'MR'
