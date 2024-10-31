from enum import StrEnum, auto


class SubscriptionPlan(StrEnum):
    ONE_WEEK_DEMO_ACCESS = auto()
    ONE_MONTH_SUBSCRIPTION = auto()
    SIX_MONTH_SUBSCRIPTION = auto()
    ONE_YEAR_SUBSCRIPTION = auto()


class MenuAction(StrEnum):
    CONNECT_VPN = auto()
    SHOW_LINKS = auto()
    CLOSE_LINKS = auto()
