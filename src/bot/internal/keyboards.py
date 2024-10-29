from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.internal.enums import SubscriptionPrice


class SubscriptionCallbackFactory(CallbackData, prefix='subscription'):
    stars_amount: SubscriptionPrice


def demo_access_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="PLATI 1 ZWEZDU",
        pay=True,
        callback_data="1z",
    )
    return builder.as_markup()


def buy_subscription_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        ("1 month", SubscriptionCallbackFactory(stars_amount=SubscriptionPrice.ONE_MONTH_SUBSCRIPTION)),
        ("6 months", SubscriptionCallbackFactory(stars_amount=SubscriptionPrice.SIX_MONTH_SUBSCRIPTION)),
        ("12 months", SubscriptionCallbackFactory(stars_amount=SubscriptionPrice.ONE_YEAR_SUBSCRIPTION)),
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def show_links_kb() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="Show links",
                callback_data="show links",
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def close_links_kb() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="Close",
                callback_data="close links",
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def connect_vpn_kb() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="Connect",
                callback_data="connect",
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
