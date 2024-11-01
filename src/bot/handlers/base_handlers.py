from datetime import UTC, datetime

from aiogram import Router
from aiogram.filters import (
    CommandStart,
)
from aiogram.types import CallbackQuery, LabeledPrice, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.controllers.crud.link import get_links_by_user_id, update_links_url
from bot.controllers.marzban import create_marzban_user, delete_marzban_user, get_marzban_token
from bot.controllers.helpers import compose_username, get_duration_string
from bot.internal.enums import MenuAction
from bot.internal.keyboards import (
    MenuCallbackFactory,
    SubscriptionCallbackFactory,
    buy_subscription_kb,
    close_links_kb,
    connect_vpn_kb, show_links_kb,
)
from bot.internal.dicts import goods, texts
from database.models import User

router = Router()


@router.message(CommandStart())
async def start(message: Message, user: User) -> None:
    current_time = datetime.now(UTC)
    markup = connect_vpn_kb()
    if not user.marzban_username:
        text = texts['no_subscription'].format(
            user_fullname=message.from_user.full_name,
            user_id=message.from_user.id,
        )
    else:
        if user.expired_at > message.date:
            delta = user.expired_at - current_time
            formatted_date = user.expired_at.strftime("%d.%m.%Y")
            text = (
                texts['user_not_expired'].format(
                    user_fullname=message.from_user.full_name,
                    user_id=message.from_user.id,
                    proxy_type='VMess',
                    valid_until=formatted_date,
                    days_left=delta.days,
                )
            )
            markup = connect_vpn_kb(with_links=True)
        else:
            text = texts['no_subscription'].format(
                user_fullname=message.from_user.full_name,
                user_id=message.from_user.id,
            )
    await message.answer(
        text=text,
        reply_markup=markup,
    )


@router.callback_query(SubscriptionCallbackFactory.filter())
async def subscription_prolongation(
    callback: CallbackQuery,
    callback_data: SubscriptionCallbackFactory,
) -> None:
    await callback.answer()
    prices = [LabeledPrice(label="XTR", amount=goods[callback_data.subscription_plan]['price'])]
    duration = get_duration_string(goods[callback_data.subscription_plan]['duration'])
    await callback.message.answer_invoice(
        title="VPN access",
        description=duration,
        payload=callback_data.subscription_plan,
        currency="XTR",
        prices=prices,
        start_parameter="stars-payment",
    )


@router.callback_query(MenuCallbackFactory.filter())
async def handle_menu_actions(
    callback: CallbackQuery,
    callback_data: MenuCallbackFactory,
    user: User,
    db_session: AsyncSession,
) -> None:
    await callback.answer()
    match callback_data.action:
        case MenuAction.SHOW_LINKS:
            links = await get_links_by_user_id(callback.from_user.id, db_session)
            await callback.message.answer(
                texts['links_message'].format(links='\n\n'.join(i.url for i in links)), reply_markup=close_links_kb()
            )
        case MenuAction.CLOSE_LINKS:
            await callback.message.delete()
        case MenuAction.CONNECT_VPN:
            await callback.message.answer(
                texts['choose_action'],
                reply_markup=close_links_kb(),
            )
        case MenuAction.RENEW_LINKS:
            # await callback.bot.send_chat_action(callback.message.chat.id, 'typing')
            marzban_token = await get_marzban_token()
            await delete_marzban_user(user.marzban_username, marzban_token)
            new_marzban_user = await create_marzban_user(
                username=compose_username(callback.message),
                tg_id=callback.from_user.id,
                token=marzban_token,
                expire=user.expired_at,
            )
            user.marzban_username = new_marzban_user.get("username")
            tcp_link, websocket_link, *_ = new_marzban_user.get("links")
            await update_links_url(callback.from_user.id, [tcp_link, websocket_link], db_session)
            await callback.message.answer(
                text=texts['links_refreshed'],
                reply_markup=show_links_kb()
            )
