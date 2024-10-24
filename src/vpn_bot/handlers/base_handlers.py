from aiogram import Router
from aiogram.filters import (
    CommandStart,
)
from aiogram.types import Message

from vpn_bot.internal.lexicon import texts

router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(texts['start_message'].format(message.from_user.full_name))
