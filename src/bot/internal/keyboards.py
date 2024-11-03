from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.internal.callbacks import DeviceCallbackFactory, MenuCallbackFactory, SubscriptionCallbackFactory
from bot.internal.enums import DeviceType, MenuAction, SubscriptionPlan


def buy_subscription_kb(demo_access_used: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    buttons = [
        ("1 week demo access", SubscriptionCallbackFactory(plan=SubscriptionPlan.ONE_WEEK_DEMO_ACCESS)),
        ("1 month", SubscriptionCallbackFactory(plan=SubscriptionPlan.ONE_MONTH_SUBSCRIPTION)),
        ("6 months", SubscriptionCallbackFactory(plan=SubscriptionPlan.SIX_MONTH_SUBSCRIPTION)),
        ("1 year", SubscriptionCallbackFactory(plan=SubscriptionPlan.ONE_YEAR_SUBSCRIPTION)),
        # ("Back", MenuCallbackFactory(action=MenuAction.BACK_TO_MENU)),
    ]
    if demo_access_used:
        del buttons[0]
    for text, callback in buttons:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def show_links_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Show links", callback_data=MenuCallbackFactory(action=MenuAction.SHOW_LINKS))
    kb.button(text="Close", callback_data=MenuCallbackFactory(action=MenuAction.CLOSE))
    kb.adjust(1)
    return kb.as_markup()


def close_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Close", callback_data=MenuCallbackFactory(action=MenuAction.CLOSE))
    return kb.as_markup()


def connect_vpn_kb(active: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Buy access", callback_data=MenuCallbackFactory(action=MenuAction.CONNECT_VPN))
    if active:
        kb.button(text="Account", callback_data=MenuCallbackFactory(action=MenuAction.ACCOUNT))
    kb.adjust(1)
    return kb.as_markup()


def account_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Setup device", callback_data=MenuCallbackFactory(action=MenuAction.SETUP_DEVICE))
    kb.button(text="Renew links", callback_data=MenuCallbackFactory(action=MenuAction.RENEW_LINKS))
    kb.button(text="Show links", callback_data=MenuCallbackFactory(action=MenuAction.SHOW_LINKS))
    kb.button(text="Back", callback_data=MenuCallbackFactory(action=MenuAction.BACK_TO_MENU))
    kb.adjust(1)
    return kb.as_markup()


def choose_device_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        ("Android", DeviceCallbackFactory(option=DeviceType.ANDROID)),
        ("iOS", DeviceCallbackFactory(option=DeviceType.IOS)),
        ("Back", MenuCallbackFactory(action=MenuAction.BACK_TO_MENU)),
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(2, 1)
    return kb.as_markup()
