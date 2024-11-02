from asyncio import sleep
import contextlib
from datetime import UTC

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import (
    CommandStart,
)
from aiogram.types import CallbackQuery, LabeledPrice, Message
from aiogram.utils.chat_action import ChatActionSender
from sqlalchemy.ext.asyncio import AsyncSession

from bot.controllers.crud.link import get_links_by_user_id, logger, update_links_url
from bot.controllers.marzban import create_marzban_user, delete_marzban_user, get_marzban_token
from bot.controllers.helpers import compose_message, get_duration_string
from bot.internal.enums import DeviceType, MenuAction, SubscriptionStatus
from bot.internal.keyboards import (
    account_kb,
    buy_subscription_kb,
    choose_device_kb,
    close_kb,
    connect_vpn_kb,
    show_links_kb,
)
from bot.internal.callbacks import DeviceCallbackFactory, MenuCallbackFactory, SubscriptionCallbackFactory
from bot.internal.dicts import goods, texts
from database.models import User

router = Router()


@router.message(CommandStart())
async def start(message: Message, user: User) -> None:
    markup = connect_vpn_kb()
    if not user.marzban_username:
        text = compose_message(user, message, SubscriptionStatus.INACTIVE)
    else:
        if user.expired_at.replace(tzinfo=UTC) > message.date.replace(tzinfo=UTC):
            text = compose_message(user, message, SubscriptionStatus.ACTIVE)
            markup = connect_vpn_kb(active=True)
        else:
            text = compose_message(user, message, SubscriptionStatus.INACTIVE)
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
    prices = [LabeledPrice(label="XTR", amount=goods[callback_data.plan]['price'])]
    duration = get_duration_string(goods[callback_data.plan]['duration'])
    await callback.message.answer_invoice(
        title="VPN access",
        description=duration,
        payload=callback_data.plan,
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
    with contextlib.suppress(TelegramBadRequest):
        match callback_data.action:
            case MenuAction.SHOW_LINKS:
                links = await get_links_by_user_id(callback.from_user.id, db_session)
                await callback.message.answer(
                    texts['links_message'].format(links='\n\n'.join(i.url for i in links)), reply_markup=close_kb()
                )
                logger.info(f"Links button pressed by user {user.username}")
            case MenuAction.CLOSE:
                await callback.message.delete()
            case MenuAction.CONNECT_VPN:
                await callback.message.edit_text(
                    texts['choose_action'],
                    reply_markup=buy_subscription_kb(user.demo_access_used),
                )
                logger.info(f"Connect VPN button pressed by user {user.username}")
            case MenuAction.RENEW_LINKS:
                async with ChatActionSender.typing(bot=callback.bot, chat_id=callback.from_user.id):
                    marzban_token = await get_marzban_token()
                    await delete_marzban_user(user.marzban_username, marzban_token)
                    await sleep(2)
                    new_marzban_user = await create_marzban_user(
                        username=user.username,
                        tg_id=callback.from_user.id,
                        token=marzban_token,
                        expire=user.expired_at,
                    )
                    user.marzban_username = new_marzban_user.get("username")
                    tcp_link, websocket_link, *_ = new_marzban_user.get("links")
                    await update_links_url(callback.from_user.id, [tcp_link, websocket_link], db_session)
                await callback.message.answer(text=texts['links_refreshed'], reply_markup=show_links_kb())
                logger.info(f"Renew links button pressed by user {user.username}")
            case MenuAction.SETUP_DEVICE:
                await callback.message.edit_text(texts['choose_device'], reply_markup=choose_device_kb())
                logger.info(f"Setup device button pressed by user {user.username}")
            case MenuAction.ACCOUNT:
                text = compose_message(user, callback.message, SubscriptionStatus.ACTIVE)
                await callback.message.edit_text(text, reply_markup=account_kb())
            case MenuAction.BACK_TO_MENU:
                text = compose_message(user, callback.message, SubscriptionStatus.ACTIVE)
                try:
                    await callback.message.edit_text(text, reply_markup=connect_vpn_kb(active=True))
                except Exception as e:
                    logger.exception(e)
                    await callback.message.answer(text, reply_markup=connect_vpn_kb(active=True))
                logger.info(f"Back to menu button pressed by user {user.username}")


@router.callback_query(DeviceCallbackFactory.filter())
async def setup_device(
    callback: CallbackQuery,
    callback_data: DeviceCallbackFactory,
    db_session: AsyncSession,
):
    await callback.answer()
    match callback_data.option:
        case DeviceType.ANDROID:
            pass
        case DeviceType.IOS:
            pass
    links = await get_links_by_user_id(callback.from_user.id, db_session)
    await callback.message.answer(
        texts['links_message'].format(links='\n\n'.join(i.url for i in links)), reply_markup=close_kb()
    )
