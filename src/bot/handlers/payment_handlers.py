from datetime import UTC, datetime
import logging

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, PreCheckoutQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import Settings
from bot.controllers.crud.user import update_db_user_expiration
from bot.internal.enums import SubscriptionPlan, SubscriptionStatus
from bot.internal.keyboards import connect_vpn_kb
from bot.internal.dicts import goods
from bot.controllers.marzban import (
    create_marzban_user,
    get_marzban_token,
    update_marzban_user_expiration,
)
from bot.internal.helpers import compose_message
from database.models import Link, User

router = Router()
logger = logging.getLogger(__name__)


@router.pre_checkout_query()
async def on_pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery,
):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def on_successful_payment(
    message: Message,
    user: User,
    settings: Settings,
    db_session: AsyncSession,
):
    payload = message.successful_payment.invoice_payload
    if payload == SubscriptionPlan.ONE_WEEK_DEMO_ACCESS:
        user.demo_access_used = True
    duration = goods[payload]['duration']
    marzban_token = await get_marzban_token(settings=settings)
    if not user.marzban_username:
        new_marzban_user = await create_marzban_user(
            username=user.username,
            tg_id=message.from_user.id,
            token=marzban_token,
            settings=settings,
            duration=duration
        )
        expire_timestamp = new_marzban_user.get("expire")
        expire_date = datetime.fromtimestamp(expire_timestamp)
        tcp_link, websocket_link, *_ = new_marzban_user.get("links")
        user.marzban_username = new_marzban_user.get("username")
        user.expired_at = expire_date.replace(tzinfo=UTC)
        db_session.add_all(
            [
                Link(user_tg_id=message.from_user.id, url=tcp_link),
                Link(user_tg_id=message.from_user.id, url=websocket_link),
            ]
        )
        text = compose_message(user, message, SubscriptionStatus.CREATED)
    else:
        await update_marzban_user_expiration(user.marzban_username, marzban_token, duration, user.expired_at)
        await update_db_user_expiration(user, duration, db_session)

        if user.expired_at.replace(tzinfo=UTC) > message.date.replace(tzinfo=UTC):
            text = compose_message(user, message, SubscriptionStatus.PROLONGED)
        else:
            text = compose_message(user, message, SubscriptionStatus.RENEWED)
    await message.answer(
        text=text,
        reply_markup=connect_vpn_kb(active=True),
    )
    logger.info(f"Successful payment for user {user.username}: {message.successful_payment.invoice_payload}")


@router.message(Command("refund"))
async def cmd_refund(
    message: Message,
    bot: Bot,
    user: User,
    settings: Settings,
    command: CommandObject,
):
    if message.from_user.id not in settings.bot.ADMINS:
        return
    transaction_id = command.args
    if transaction_id is None:
        await message.answer("No refund code provided")
        return
    try:
        await bot.refund_star_payment(user_id=message.from_user.id, telegram_payment_charge_id=transaction_id)
        await message.answer("Refund successful")
        logger.info(f"Refund for user {user.username} successful: {transaction_id}")
    except TelegramBadRequest as error:
        if "CHARGE_NOT_FOUND" in error.message:
            text = "Refund code not found"
        elif "CHARGE_ALREADY_REFUNDED" in error.message:
            text = "Stars already refunded"
        else:
            text = "Refund code not found"
        await message.answer(text)
        logger.exception(error.message)
        return
