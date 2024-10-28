from datetime import datetime

from aiogram import Router
from aiogram.filters import (
    CommandStart,
)
from aiogram.types import LabeledPrice, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.internal.enums import SubscriptionPrice
from bot.internal.keyboards import demo_access_kb
from bot.internal.lexicon import texts
from bot.controllers.crud.user import get_user_from_db_by_tg_id

router = Router()


@router.message(CommandStart())
async def start(message: Message, db_session: AsyncSession) -> None:
    user = await get_user_from_db_by_tg_id(message.from_user.id, db_session)
    current_time = datetime.now()
    if not user:
        await message.answer(texts['start_message'].format(
            user_fullname=message.from_user.full_name,
        ))
        prices = [LabeledPrice(label="XTR", amount=SubscriptionPrice.ONE_WEEK_DEMO_ACCESS.value)]
        await message.answer_invoice(
            title="Demo access to VPN",
            description="For access to VPN, please purchase a subscription",
            payload="payment for VPN",
            currency="XTR",
            prices=prices,
            start_parameter="stars-payment",
        )
    else:
        if user.expired_at > message.date:
            delta = user.expired_at - current_time
            await message.answer(texts['start_message'].format(
                user_fullname=message.from_user.full_name,
                user_id=message.from_user.id,
                status='Inactive',
                proxy_type='VMess',
                valid_until=user.expired_at,
                days_left=delta.days
            ))
        else:
            prices = [
                LabeledPrice(label="XTR", amount=SubscriptionPrice.ONE_MONTH_SUBSCRIPTION.value),
                LabeledPrice(label="XTR", amount=SubscriptionPrice.SIX_MONTH_SUBSCRIPTION.value),
                LabeledPrice(label="XTR", amount=SubscriptionPrice.ONE_YEAR_SUBSCRIPTION.value)
            ]
            await message.answer_invoice(
                title="Add more time",
                description="For access to VPN, please purchase a subscription",
                payload="payment for VPN",
                currency="XTR",
                prices=prices,
                start_parameter="stars-payment",
            )
            # await message.answer(
            #     texts['start_message'].format(message.from_user.full_name), reply_markup=demo_access_kb()
            # )
