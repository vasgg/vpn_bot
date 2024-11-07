from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.internal.callbacks import DeviceCallbackFactory, HelpCallbackFactory, MenuCallbackFactory, \
    SubscriptionCallbackFactory
from bot.internal.enums import DeviceType, HelpMenuAction, MainMenuAction, SubscriptionPlan


class MenuButton:
    ACCESS_1_WEEK = "🎁 1 week demo access", SubscriptionCallbackFactory(plan=SubscriptionPlan.ONE_WEEK_DEMO_ACCESS)
    ACCESS_1_MONTH = "1 month", SubscriptionCallbackFactory(plan=SubscriptionPlan.ONE_MONTH_SUBSCRIPTION)
    ACCESS_6_MONTH = "6 months", SubscriptionCallbackFactory(plan=SubscriptionPlan.SIX_MONTH_SUBSCRIPTION)
    ACCESS_1_YEAR = "1 year", SubscriptionCallbackFactory(plan=SubscriptionPlan.ONE_YEAR_SUBSCRIPTION)
    CONNECT_VPN = "🚀 Buy access", MenuCallbackFactory(action=MainMenuAction.CONNECT_VPN)
    SHOW_LINKS = "📄 Show links", MenuCallbackFactory(action=MainMenuAction.SHOW_LINKS)
    ACCOUNT = "⚙️ Account", MenuCallbackFactory(action=MainMenuAction.ACCOUNT)
    RENEW_LINKS = "🔄 Renew links", MenuCallbackFactory(action=MainMenuAction.RENEW_LINKS)
    CLOSE = "❌ Close", MenuCallbackFactory(action=MainMenuAction.CLOSE)
    HELP = "🆘 Help", MenuCallbackFactory(action=MainMenuAction.HELP)
    BACK_TO_MENU = "⬅️ Back", MenuCallbackFactory(action=MainMenuAction.BACK_TO_MENU)


class HelpButton:
    BACK_TO_HELP = "⬅️ Back", HelpCallbackFactory(action=HelpMenuAction.BACK_TO_HELP)
    SETUP_DEVICE = "📱 Setup device", HelpCallbackFactory(action=HelpMenuAction.SETUP_DEVICE)
    PAYMENT_WITH_STARS = "Payment with stars", HelpCallbackFactory(action=HelpMenuAction.STARS)
    CONTACT_SUPPORT = "📞 Contact support", HelpCallbackFactory(action=HelpMenuAction.CONTACT_SUPPORT)
    LOW_SPEED = "Low internet speed", HelpCallbackFactory(action=HelpMenuAction.LOW_SPEED)
    VPN_NOT_WORKING = "VPN not working", HelpCallbackFactory(action=HelpMenuAction.VPN_NOT_WORKING)


def buy_subscription_kb(demo_access_used: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    buttons = [
        MenuButton.ACCESS_1_WEEK,
        MenuButton.ACCESS_1_MONTH,
        MenuButton.ACCESS_6_MONTH,
        MenuButton.ACCESS_1_YEAR,
        MenuButton.BACK_TO_MENU,
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
        HelpButton.SETUP_DEVICE,
        HelpButton.VPN_NOT_WORKING,
        HelpButton.PAYMENT_WITH_STARS,
        HelpButton.LOW_SPEED,
        HelpButton.CONTACT_SUPPORT,
        MenuButton.BACK_TO_MENU,
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def show_links_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        MenuButton.SHOW_LINKS,
        MenuButton.CLOSE,
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def close_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=MenuButton.CLOSE[0], callback_data=MenuButton.CLOSE[1])
    return kb.as_markup()


def back_to_help_kb(setup_device: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if setup_device:
        kb.button(text=HelpButton.SETUP_DEVICE[0], callback_data=HelpButton.SETUP_DEVICE[1])
    kb.button(text=HelpButton.BACK_TO_HELP[0], callback_data=HelpButton.BACK_TO_HELP[1])
    kb.adjust(1)
    return kb.as_markup()


def connect_vpn_kb(active: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=MenuButton.CONNECT_VPN[0], callback_data=MenuButton.CONNECT_VPN[1])
    if active:
        kb.button(text=MenuButton.ACCOUNT[0], callback_data=MenuButton.ACCOUNT[1])
    kb.button(text=MenuButton.HELP[0], callback_data=MenuButton.HELP[1])
    kb.adjust(1)
    return kb.as_markup()


def account_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        MenuButton.SHOW_LINKS,
        MenuButton.RENEW_LINKS,
        MenuButton.BACK_TO_MENU,
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def choose_device_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='iOS', url='https://teletype.in/@info_vpn/yLRxvXYMoM-')
    kb.button(text='Android', url='https://teletype.in/@info_vpn/yLRxvXYMoM-')
    kb.button(text=HelpButton.BACK_TO_HELP[0], callback_data=HelpButton.BACK_TO_HELP[1])
    kb.adjust(2, 1)
    return kb.as_markup()
