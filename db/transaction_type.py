from enum import StrEnum, auto


class TransactionType(StrEnum):
    BY_CARD = auto()
    BY_CASH = auto()
