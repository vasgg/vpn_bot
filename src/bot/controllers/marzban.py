import asyncio
from asyncio import sleep
from datetime import UTC, datetime
import logging
from uuid import uuid4

from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from dateutil.relativedelta import relativedelta
import httpx
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import Settings, MarzbanConfig
from bot.controllers.crud.link import update_links_url
from bot.internal.helpers import pink_convert
from database.models import User

logger = logging.getLogger(__name__)


async def get_marzban_token(marzban: MarzbanConfig) -> str:
    url = f"{marzban.BASE_URL}/api/admin/token"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "username": marzban.ADMIN,
        "password": marzban.PASSWORD.get_secret_value(),
    }
    logger.info(f"Data: {data}")
    logger.info(f"Headers: {headers}")
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=data)
        try:
            response.raise_for_status()
            logger.info(f"Obtaining Marzban token. Server response: {response.json()}")
            token_data = response.json()
            return token_data.get("access_token")
        except httpx.HTTPStatusError as e:
            logger.exception(f"Obtaining Marzban token. Server response with error: {response.json()}, error: {e}")
            raise


async def create_marzban_user(
    username: str,
    tg_id: int,
    token: str,
    settings: Settings,
    duration: relativedelta | None = None,
    expire: datetime | None = None,
) -> dict:
    url = f"{settings.marzban.BASE_URL}/api/user"
    if duration:
        expire_date = datetime.now(UTC) + duration
        expire_timestamp = int(expire_date.timestamp())
    else:
        expire_timestamp = int(expire.timestamp())
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = {
        "username": pink_convert(username),
        "expire": expire_timestamp,
        "note": f"Telegram user: {username}, tg_id: {tg_id}",
        "proxies": {"vmess": {"id": str(uuid4())}},
        "inbounds": {
            "vmess": [
                "VMESS + TCP",
                "VMESS + WS"
            ],
            "vless": [
                "VLESS + TCP",
                "VLESS + WS"
            ]
        },
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        try:
            response.raise_for_status()
            logger.info(f"Creating new Marzban user. Server response: {response.json()}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.exception(f"Creating new Marzban user. Server response with error: {response.json()}, error: {e}")
            raise


async def delete_marzban_user(username: str, token: str, settings: Settings) -> dict:
    url = f"{settings.marzban.BASE_URL}/api/user/{username}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)
        try:
            response.raise_for_status()
            logger.info(f"Deleting Marzban user: {username}. Server response: {response.json()}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.exception(
                f"Deleting Marzban user: {username}. " f"Server response with error: {response.json()}, error: {e}"
            )
            raise


async def get_marzban_user(username: str, token: str, settings: Settings) -> dict:
    url = f"{settings.marzban.BASE_URL}/api/user/{username}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        try:
            response.raise_for_status()
            logger.info(f"Server response: {response.json()}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.exception(f"Server response with error: {response.json()}, error: {e}")
            raise


async def update_marzban_user_expiration(
    username: str,
    token: str,
    settings: Settings,
    duration: relativedelta,
    user_expired_at: datetime,
) -> dict:
    url = f"{settings.marzban.BASE_URL}/api/user/{username}"
    now = datetime.now(UTC)
    if user_expired_at.tzinfo is None:
        user_expired_at = user_expired_at.replace(tzinfo=UTC)
    if user_expired_at < now:
        expire_date = now + duration
        expire_timestamp = int(expire_date.timestamp())
    else:
        expire_date = user_expired_at + duration
        expire_timestamp = int(expire_date.timestamp())
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = {"expire": expire_timestamp}
    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=headers, json=data)
        try:
            response.raise_for_status()
            logger.info(f"Updating Marzban user expiration for {username}. Server response: {response.json()}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.exception(
                f"Updating Marzban user expiration for {username}. "
                f"Server response with error: {response.json()}, error: {e}"
            )
            raise


async def renew_links(message: Message, user: User, settings: Settings, db_session: AsyncSession):
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.from_user.id):
        marzban_token = await get_marzban_token(settings.marzban)
        await delete_marzban_user(user.marzban_username, marzban_token, settings)
        await sleep(2)
        new_marzban_user = await create_marzban_user(
            username=user.username,
            tg_id=message.from_user.id,
            token=marzban_token,
            settings=settings,
            expire=user.expired_at,
        )
        user.marzban_username = new_marzban_user.get("username")
        tcp_link, websocket_link, *_ = new_marzban_user.get("links")
        await update_links_url(user.tg_id, [tcp_link, websocket_link], db_session)


async def main():
    marz = MarzbanConfig(BASE_URL="http://localhost:8000", ADMIN="horokey", PASSWORD=SecretStr("7f4df451"))
    token = await get_marzban_token(marz)
    print(token)

if __name__ == '__main__':
    asyncio.run(main())