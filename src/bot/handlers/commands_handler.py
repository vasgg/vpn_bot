from datetime import UTC

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import Settings
from bot.controllers.crud.link import logger
from bot.controllers.marzban import renew_links
from bot.internal.helpers import compose_message
from bot.internal.enums import SubscriptionStatus
from bot.internal.keyboards import (
    account_kb,
    buy_subscription_kb,
    connect_vpn_kb,
    help_menu_kb,
    show_links_kb,
)
from bot.internal.dicts import texts
from database.models import User


router = Router()


@router.message(Command("start", "connect_vpn", "renew_links", "account", "help"))
async def command_handler(
    message: Message,
    command: CommandObject,
    user: User,
    settings: Settings,
    user_active: bool,
    db_session: AsyncSession,
) -> None:
    match command.command:
        case "start":
            markup = connect_vpn_kb()
            if not user.marzban_username:
                text = compose_message(user, message, SubscriptionStatus.INACTIVE)
            else:
                if user.expired_at.replace(tzinfo=UTC) > message.date.replace(tzinfo=UTC):
                    text = compose_message(user, message, SubscriptionStatus.ACTIVE)
                    markup = connect_vpn_kb(active=True)
                else:
                    text = compose_message(user, message, SubscriptionStatus.INACTIVE)
            logger.info(f"Start command called by user {user.username}")
        case "connect_vpn":
            text = texts['choose_plan']
            markup = buy_subscription_kb(user.demo_access_used)
            logger.info(f"Connect VPN command called by user {user.username}")
        case "renew_links":
            await renew_links(message, user, settings, db_session)
            text = texts['links_refreshed']
            markup = show_links_kb()
            logger.info(f"Renew links command called by user {user.username}")
        case "account":
            user_status = SubscriptionStatus.ACTIVE if user_active else SubscriptionStatus.INACTIVE
            text = compose_message(user, message, user_status)
            markup = account_kb()
            logger.info(f"Account command called by user {user.username}")
        case "help":
            text = texts['help'].format(user_id=user.tg_id)
            markup = help_menu_kb()
            logger.info(f"Help command called by user {user.username}")
        case _:
            assert False, "Unexpected command"
    await message.answer(
        text=text,
        reply_markup=markup,
    )
