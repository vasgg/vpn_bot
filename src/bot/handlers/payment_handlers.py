from datetime import datetime

from aiogram import Bot, F, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from sqlalchemy.ext.asyncio import AsyncSession

from bot.internal.lexicon import texts
from bot.controllers.marzban import create_marzban_user, get_marzban_token
from bot.controllers.crud.user import get_user_from_db_by_tg_id
from database.models import Link, User

router = Router()


@router.pre_checkout_query()
async def on_pre_checkout_query(
    pre_checkout_query: types.PreCheckoutQuery,
):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def on_successful_payment(
    message: types.Message,
    db_session: AsyncSession,
):
    await message.answer(
        f"payment successful!",
        message_effect_id="5104841245755180586",
    )
    user = await get_user_from_db_by_tg_id(message.from_user.id, db_session)
    marzban_secret_token = await get_marzban_token()
    if not user:
        username = (
            '@' + message.from_user.username
            if message.from_user.username
            else message.from_user.full_name.replace(' ', '_')
        )
        new_marzban_user = await create_marzban_user(username, message.from_user.id, marzban_secret_token)
        expire_timestamp = new_marzban_user.get("expire")
        expire_date = datetime.fromtimestamp(expire_timestamp)
        current_timestamp = int(datetime.now().timestamp())
        days_left = (expire_timestamp - current_timestamp) // (24 * 3600)
        tcp_link = new_marzban_user.get("links")[0]
        websocket_link = new_marzban_user.get("links")[1]
        await message.answer(
            texts['user_created'].format(
                user_fullname=message.from_user.full_name,
                user_id=message.from_user.id,
                status=new_marzban_user.get("status"),
                proxy_type='VMess',
                valid_until=expire_date.strftime("%d.%m.%Y"),
                days_left=days_left,
            )
        )
        await message.answer(
            texts['links_message'].format(
                link1=tcp_link,
                link2=websocket_link,
            )
        )
        new_user = User(
            tg_id=message.from_user.id,
            fullname=message.from_user.full_name,
            username=message.from_user.username,
            expired_at=expire_date,
        )
        new_tcp_link = Link(
            user_marzban_id=new_marzban_user["proxies"]["vmess"]["id"],
            user_tg_id=message.from_user.id,
            url=tcp_link,
        )
        new_websocket_link = Link(
            user_marzban_id=new_marzban_user["proxies"]["vmess"]["id"],
            user_tg_id=message.from_user.id,
            url=websocket_link,
        )
        db_session.add(new_user)
        await db_session.flush()
        db_session.add_all([new_tcp_link, new_websocket_link])
    else:
        await message.answer(
            texts['user_already_exists'].format(
                user_fullname=message.from_user.full_name,
                user_id=message.from_user.id,
            )
        )


@router.message(Command("refund"))
async def cmd_refund(
    message: types.Message,
    bot: Bot,
    command: CommandObject,
):
    transaction_id = command.args
    if transaction_id is None:
        await message.answer("no refund code provided")
        return
    try:
        await bot.refund_star_payment(user_id=message.from_user.id, telegram_payment_charge_id=transaction_id)
        await message.answer("refund successful", message_effect_id='5046589136895476101')
    except TelegramBadRequest as error:
        if "CHARGE_NOT_FOUND" in error.message:
            text = "refund code not found"
        elif "CHARGE_ALREADY_REFUNDED" in error.message:
            text = "refund already refunded"
        else:
            text = "refund code not found"
        await message.answer(text)
        return
