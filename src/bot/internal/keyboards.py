from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.internal.callbacks import DeviceCallbackFactory, MenuCallbackFactory, SubscriptionCallbackFactory
from bot.internal.enums import DeviceType, MenuAction, SubscriptionPlan


class Button:
    ACCESS_1_WEEK = "🎁 1 week demo access", SubscriptionCallbackFactory(plan=SubscriptionPlan.ONE_WEEK_DEMO_ACCESS)
    ACCESS_1_MONTH = "1 month", SubscriptionCallbackFactory(plan=SubscriptionPlan.ONE_MONTH_SUBSCRIPTION)
    ACCESS_6_MONTH = "6 months", SubscriptionCallbackFactory(plan=SubscriptionPlan.SIX_MONTH_SUBSCRIPTION)
    ACCESS_1_YEAR = "1 year", SubscriptionCallbackFactory(plan=SubscriptionPlan.ONE_YEAR_SUBSCRIPTION)
    ANDROID = "Android", DeviceCallbackFactory(option=DeviceType.ANDROID)
    IOS = "iOS", DeviceCallbackFactory(option=DeviceType.IOS)
    CONNECT_VPN = "🚀 Buy access", MenuCallbackFactory(action=MenuAction.CONNECT_VPN)
    SHOW_LINKS = "📄 Show links", MenuCallbackFactory(action=MenuAction.SHOW_LINKS)
    BACK_TO_MENU = "⬅️ Back", MenuCallbackFactory(action=MenuAction.BACK_TO_MENU)
    ACCOUNT = "⚙️ Account", MenuCallbackFactory(action=MenuAction.ACCOUNT)
    SETUP_DEVICE = "📱 Setup device", MenuCallbackFactory(action=MenuAction.SETUP_DEVICE)
    RENEW_LINKS = "🔄 Renew links", MenuCallbackFactory(action=MenuAction.RENEW_LINKS)
    CLOSE = "❌ Close", MenuCallbackFactory(action=MenuAction.CLOSE)
    HELP = "🆘 Help", MenuCallbackFactory(action=MenuAction.HELP)
    CONTACT_SUPPORT = "📞 Contact support", MenuCallbackFactory(action=MenuAction.CONTACT_SUPPORT)


def buy_subscription_kb(demo_access_used: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    buttons = [
        Button.ACCESS_1_WEEK,
        Button.ACCESS_1_MONTH,
        Button.ACCESS_6_MONTH,
        Button.ACCESS_1_YEAR,
        Button.BACK_TO_MENU,
    ]
    if demo_access_used:
        del buttons[0]
    for text, callback in buttons:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def help_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        Button.SETUP_DEVICE,
        Button.CONTACT_SUPPORT,
        Button.BACK_TO_MENU,
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def show_links_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        Button.SHOW_LINKS,
        Button.CLOSE,
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def close_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=Button.CLOSE[0], callback_data=Button.CLOSE[1])
    return kb.as_markup()


def connect_vpn_kb(active: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=Button.CONNECT_VPN[0], callback_data=Button.CONNECT_VPN[1])
    if active:
        kb.button(text=Button.ACCOUNT[0], callback_data=Button.ACCOUNT[1])
    kb.button(text=Button.HELP[0], callback_data=Button.HELP[1])
    kb.adjust(1)
    return kb.as_markup()


def account_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        Button.SHOW_LINKS,
        Button.RENEW_LINKS,
        Button.BACK_TO_MENU,
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def choose_device_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        Button.ANDROID,
        Button.IOS,
        Button.BACK_TO_MENU,
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(2, 1)
    return kb.as_markup()
