from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, PreCheckoutQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.internal.enums import SubscriptionPrice
from bot.internal.keyboards import show_links_kb
from bot.internal.lexicon import texts
from bot.controllers.marzban import create_marzban_user, get_marzban_token, process_subscription
from bot.controllers.crud.user import get_user_from_db_by_tg_id, update_user_expiration
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
    db_session: AsyncSession,
):
    user = await get_user_from_db_by_tg_id(message.from_user.id, db_session)
    payment_info = message.successful_payment
    total_amount = payment_info.total_amount
    current_timestamp = int(datetime.now().timestamp())
    username = (
        '@' + message.from_user.username
        if message.from_user.username
        else message.from_user.full_name.replace(' ', '_')
    )
    if total_amount == SubscriptionPrice.ONE_WEEK_DEMO_ACCESS:
        if not user:
            marzban_secret_token = await get_marzban_token()
            new_marzban_user = await create_marzban_user(username, message.from_user.id, marzban_secret_token)
            expire_timestamp = new_marzban_user.get("expire")
            expire_date = datetime.fromtimestamp(expire_timestamp)
            days_left = (expire_timestamp - current_timestamp) // (24 * 3600)
            tcp_link, websocket_link, *_ = new_marzban_user.get("links")

            new_user = User(
                tg_id=message.from_user.id,
                fullname=message.from_user.full_name,
                username=message.from_user.username,
                marzban_username=new_marzban_user.get("username"),
                demo_access_used=True,
                expired_at=expire_date,
            )
            db_session.add(new_user)
            await db_session.flush()

            db_session.add_all(
                [
                    Link(user_tg_id=message.from_user.id, url=tcp_link),
                    Link(user_tg_id=message.from_user.id, url=websocket_link),
                ]
            )

            text = texts['user_created'].format(
                user_fullname=message.from_user.full_name,
                user_id=message.from_user.id,
                status=new_marzban_user.get("status"),
                proxy_type='VMess',
                valid_until=expire_date.strftime("%d.%m.%Y"),
                days_left=days_left,
            )
    else:
        match total_amount:
            case SubscriptionPrice.ONE_MONTH_SUBSCRIPTION:
                text = await process_subscription(user, 1, current_timestamp, db_session)
            case SubscriptionPrice.SIX_MONTH_SUBSCRIPTION:
                text = await process_subscription(user, 6, current_timestamp, db_session)
            case SubscriptionPrice.ONE_YEAR_SUBSCRIPTION:
                text = await process_subscription(user, 12, current_timestamp, db_session)
            case _:
                raise ValueError(f"Unexpected total_amount: {total_amount}")

    await message.answer(
        text=text,
        reply_markup=show_links_kb(),
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
