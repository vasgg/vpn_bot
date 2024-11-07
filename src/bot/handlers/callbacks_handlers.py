import contextlib

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, LabeledPrice
from sqlalchemy.ext.asyncio import AsyncSession

from bot.controllers.crud.link import get_links_by_user_id, logger
from bot.controllers.marzban import renew_links
from bot.internal.helpers import compose_message, get_duration_string
from bot.internal.enums import HelpMenuAction, MainMenuAction, SubscriptionStatus
from bot.internal.keyboards import (
    account_kb,
    back_to_help_kb,
    buy_subscription_kb,
    choose_device_kb,
    close_kb,
    connect_vpn_kb,
    help_menu_kb,
    show_links_kb,
)
from bot.internal.callbacks import (
    HelpCallbackFactory,
    MenuCallbackFactory,
    SubscriptionCallbackFactory,
)
from bot.internal.dicts import goods, texts
from database.models import User

router = Router()


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
    user_active: bool,
    db_session: AsyncSession,
) -> None:
    await callback.answer()
    user_status = SubscriptionStatus.ACTIVE if user_active else SubscriptionStatus.INACTIVE
    with contextlib.suppress(TelegramBadRequest):
        match callback_data.action:
            case MainMenuAction.SHOW_LINKS:
                links = await get_links_by_user_id(user.tg_id, db_session)
                await callback.message.answer(
                    texts['links_message'].format(links='\n\n'.join(i.url for i in links)), reply_markup=close_kb()
                )
                logger.info(f"Links button pressed by user {user.username}")
            case MainMenuAction.CONNECT_VPN:
                await callback.message.edit_text(
                    texts['choose_plan'],
                    reply_markup=buy_subscription_kb(user.demo_access_used),
                )
                logger.info(f"Connect VPN button pressed by user {user.username}")
            case MainMenuAction.RENEW_LINKS:
                await renew_links(callback.message, user, db_session)
                await callback.message.answer(text=texts['links_refreshed'], reply_markup=show_links_kb())
                logger.info(f"Renew links button pressed by user {user.username}")
            case MainMenuAction.ACCOUNT:
                text = compose_message(user, callback.message, user_status)
                await callback.message.edit_text(text, reply_markup=account_kb())
                logger.info(f"Account button pressed by user {user.username}")
            case MainMenuAction.BACK_TO_MENU:
                text = compose_message(user, callback.message, user_status)
                try:
                    await callback.message.edit_text(text, reply_markup=connect_vpn_kb(active=user_active))
                except Exception as e:
                    logger.exception(e)
                    await callback.message.answer(text, reply_markup=connect_vpn_kb(active=user_active))
                logger.info(f"Back to menu button pressed by user {user.username}")
            case MainMenuAction.HELP:
                await callback.message.edit_text(texts['help'].format(user_id=user.tg_id), reply_markup=help_menu_kb())
                logger.info(f"Help button pressed by user {user.username}")
            case MainMenuAction.CLOSE:
                await callback.message.delete()


@router.callback_query(HelpCallbackFactory.filter())
async def handle_help_menu_actions(
    callback: CallbackQuery,
    callback_data: HelpCallbackFactory,
    user: User,
) -> None:
    await callback.answer()
    with contextlib.suppress(TelegramBadRequest):
        match callback_data.action:
            case HelpMenuAction.SETUP_DEVICE:
                await callback.message.edit_text(texts['choose_device'], reply_markup=choose_device_kb())
                logger.info(f"Setup device button pressed by user {user.username}")
            case HelpMenuAction.CONTACT_SUPPORT:
                await callback.message.edit_text(texts['support'], reply_markup=back_to_help_kb())
            case HelpMenuAction.VPN_NOT_WORKING:
                await callback.message.edit_text(
                    texts['vpn_not_working'], reply_markup=back_to_help_kb(setup_device=True)
                )
            case HelpMenuAction.STARS:
                await callback.message.edit_text(texts['stars'], reply_markup=back_to_help_kb())
            case HelpMenuAction.LOW_SPEED:
                await callback.message.edit_text(texts['low_speed'], reply_markup=back_to_help_kb())
            case HelpMenuAction.BACK_TO_HELP:
                try:
                    await callback.message.edit_text(
                        texts['help'].format(user_id=user.tg_id), reply_markup=help_menu_kb()
                    )
                except Exception as e:
                    logger.exception(e)
                    await callback.message.answer(
                        texts['help'].format(user_id=user.tg_id), reply_markup=help_menu_kb()
                    )
                logger.info(f"Back to menu button pressed by user {user.username}")
                await callback.message.edit_text(texts['help'].format(user_id=user.tg_id), reply_markup=help_menu_kb())
