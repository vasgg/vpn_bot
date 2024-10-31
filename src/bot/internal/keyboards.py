from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.internal.enums import MenuAction, SubscriptionPlan


class SubscriptionCallbackFactory(CallbackData, prefix='subscription'):
    subscription_plan: SubscriptionPlan


class MenuCallbackFactory(CallbackData, prefix='menu'):
    action: MenuAction


def buy_subscription_kb(demo_access_used: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    buttons = [
        ("1 week", SubscriptionCallbackFactory(subscription_plan=SubscriptionPlan.ONE_WEEK_DEMO_ACCESS)),
        ("1 month", SubscriptionCallbackFactory(subscription_plan=SubscriptionPlan.ONE_MONTH_SUBSCRIPTION)),
        ("6 months", SubscriptionCallbackFactory(subscription_plan=SubscriptionPlan.SIX_MONTH_SUBSCRIPTION)),
        ("1 year", SubscriptionCallbackFactory(subscription_plan=SubscriptionPlan.ONE_YEAR_SUBSCRIPTION)),
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
    return kb.as_markup()


def close_links_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Connect VPN", callback_data=MenuCallbackFactory(action=MenuAction.CLOSE_LINKS))
    return kb.as_markup()


def connect_vpn_kb(with_links: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Connect VPN", callback_data=MenuCallbackFactory(action=MenuAction.CONNECT_VPN))
    if with_links:
        kb.button(text="Show links", callback_data=MenuCallbackFactory(action=MenuAction.SHOW_LINKS))
    kb.adjust(1)
    return kb.as_markup()
