from aiogram import Router
from aiogram.filters import (
    CommandStart,
)
from aiogram.types import LabeledPrice, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.internal.keyboards import demo_access_kb
from bot.internal.lexicon import texts
from bot.controllers.crud.user import get_user_from_db_by_tg_id

router = Router()


@router.message(CommandStart())
async def start(message: Message, db_session: AsyncSession) -> None:
    # await message.answer(texts['start_message'].format(message.from_user.full_name))
    user = await get_user_from_db_by_tg_id(message.from_user.id, db_session)
    if not user:
        prices = [LabeledPrice(label="XTR", amount=1)]
        await message.answer_invoice(
            title="Access to VPN",
            description="For access to VPN, please purchase a subscription",
            payload="payment for VPN",
            currency="XTR",
            prices=prices,
            start_parameter="stars-payment",
        )
    else:
        # TODO: check if user is expired
        if user.expired_at < message.date:
            await message.answer('main menu\n\nyour ID is {}'.format(message.from_user.id))
        else:
            await message.answer(
                texts['start_message'].format(message.from_user.full_name), reply_markup=demo_access_kb()
            )
