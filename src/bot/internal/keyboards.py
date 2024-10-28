from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def demo_access_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="PLATI 1 ZWEZDU",
        pay=True,
        callback_data="1z",
    )
    return builder.as_markup()
