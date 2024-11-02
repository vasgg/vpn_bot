from enum import StrEnum, auto


class SubscriptionPlan(StrEnum):
    ONE_WEEK_DEMO_ACCESS = auto()
    ONE_MONTH_SUBSCRIPTION = auto()
    SIX_MONTH_SUBSCRIPTION = auto()
    ONE_YEAR_SUBSCRIPTION = auto()


class MenuAction(StrEnum):
    CONNECT_VPN = auto()
    SHOW_LINKS = auto()
    CLOSE = auto()
    RENEW_LINKS = auto()
    SETUP_DEVICE = auto()
    ACCOUNT = auto()
    BACK_TO_MENU = auto()


class DeviceType(StrEnum):
    ANDROID = auto()
    IOS = auto()


class Stage(StrEnum):
    DEV = auto()
    PROD = auto()


class SubscriptionStatus(StrEnum):
    INACTIVE = auto()
    ACTIVE = auto()
    CREATED = auto()
    RENEWED = auto()
    PROLONGED = auto()
