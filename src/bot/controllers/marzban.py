from datetime import UTC, datetime
import logging
from uuid import uuid4

from dateutil.relativedelta import relativedelta
import httpx

from bot.config import settings
from bot.controllers.helpers import pink_convert

logger = logging.getLogger(__name__)


async def get_marzban_token() -> str:
    url = f"{settings.marzban.BASE_URL}/api/admin/token"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "username": settings.marzban.ADMIN,
        "password": settings.marzban.PASSWORD.get_secret_value(),
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get("access_token")


async def create_marzban_user(
    username: str, tg_id: int, token: str, duration: relativedelta | None = None, expire: datetime | None = None
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


async def delete_marzban_user(username: str, token: str) -> dict:
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


async def get_marzban_user(username: str, token: str) -> dict:
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
    username: str, token: str, duration: relativedelta, user_expired_at: datetime
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
