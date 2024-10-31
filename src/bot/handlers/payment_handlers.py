from datetime import UTC, datetime

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, PreCheckoutQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.controllers.crud.user import update_db_user_expiration
from bot.internal.enums import SubscriptionPlan
from bot.internal.keyboards import connect_vpn_kb
from bot.internal.dicts import goods, texts
from bot.controllers.marzban import (
    create_marzban_user,
    get_duration_string, get_marzban_token,
    update_marzban_user_expiration,
)
from database.models import Link, User

router = Router()


@router.pre_checkout_query()
async def on_pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery,
):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def on_successful_payment(
    message: Message,
    user: User,
    db_session: AsyncSession,
):
    username = (
        '@' + message.from_user.username
        if message.from_user.username
        else message.from_user.full_name.replace(' ', '_')
    )
    current_timestamp = int(datetime.now(UTC).timestamp())
    payload = message.successful_payment.invoice_payload
    if payload == SubscriptionPlan.ONE_WEEK_DEMO_ACCESS:
        user.demo_access_used = True
    duration = goods[payload]['duration']
    marzban_token = await get_marzban_token()
    if not user.marzban_username:
        new_marzban_user = await create_marzban_user(username, message.from_user.id, marzban_token, duration)
        expire_timestamp = new_marzban_user.get("expire")
        expire_date = datetime.fromtimestamp(expire_timestamp)
        days_left = (expire_timestamp - current_timestamp) // (24 * 3600)
        tcp_link, websocket_link, *_ = new_marzban_user.get("links")
        user.marzban_username = new_marzban_user.get("username")
        user.expired_at = expire_date
        db_session.add_all(
            [
                Link(user_tg_id=message.from_user.id, url=tcp_link),
                Link(user_tg_id=message.from_user.id, url=websocket_link),
            ]
        )
        text = texts['user_created'].format(
            user_fullname=message.from_user.full_name,
            user_id=message.from_user.id,
            proxy_type='VMess',
            valid_until=expire_date.strftime("%d.%m.%Y"),
            days_left=days_left,
        )
    else:
        await update_marzban_user_expiration(user.marzban_username, marzban_token, duration, user.expired_at)
        await update_db_user_expiration(user, duration, db_session)

        if user.expired_at > message.date:
            text = texts['prolong_subscription'].format(
                added_time=get_duration_string(duration),
                user_id=message.from_user.id,
                proxy_type='VMess',
                valid_until=user.expired_at.strftime("%d.%m.%Y"),
                days_left=(user.expired_at - message.date).days,
            )
        else:
            text = texts['renew_subscription'].format(
                added_time=get_duration_string(duration),
                user_id=message.from_user.id,
                proxy_type='VMess',
                valid_until=user.expired_at.strftime("%d.%m.%Y"),
                days_left=(user.expired_at - message.date).days,
            )
    await message.answer(
        text=text,
        reply_markup=connect_vpn_kb(with_links=True),
    )


@router.message(Command("refund"))
async def cmd_refund(
    message: Message,
    bot: Bot,
    command: CommandObject,
):
    transaction_id = command.args
    if transaction_id is None:
        await message.answer("No refund code provided")
        return
    try:
        await bot.refund_star_payment(user_id=message.from_user.id, telegram_payment_charge_id=transaction_id)
        await message.answer("Refund successful")
    except TelegramBadRequest as error:
        if "CHARGE_NOT_FOUND" in error.message:
            text = "Refund code not found"
        elif "CHARGE_ALREADY_REFUNDED" in error.message:
            text = "Stars already refunded"
        else:
            text = "Refund code not found"
        await message.answer(text)
        return
