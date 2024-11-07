from enum import StrEnum, auto


class SubscriptionPlan(StrEnum):
    ONE_WEEK_DEMO_ACCESS = auto()
    ONE_MONTH_SUBSCRIPTION = auto()
    SIX_MONTH_SUBSCRIPTION = auto()
    ONE_YEAR_SUBSCRIPTION = auto()


class MainMenuAction(StrEnum):
    CONNECT_VPN = auto()
    SHOW_LINKS = auto()
    RENEW_LINKS = auto()
    ACCOUNT = auto()
    HELP = auto()
    CLOSE = auto()
    BACK_TO_MENU = auto()


class HelpMenuAction(StrEnum):
    SETUP_DEVICE = auto()
    CONTACT_SUPPORT = auto()
    VPN_NOT_WORKING = auto()
    STARS = auto()
    LOW_SPEED = auto()
    BACK_TO_HELP = auto()


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
