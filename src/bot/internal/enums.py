from enum import IntEnum, StrEnum, auto


class Stage(StrEnum):
    PROD = auto()
    DEV = auto()


class SubscriptionPrice(IntEnum):
    ONE_WEEK_DEMO_ACCESS = 1
    ONE_MONTH_SUBSCRIPTION = 10
    SIX_MONTH_SUBSCRIPTION = 20
    ONE_YEAR_SUBSCRIPTION = 30
