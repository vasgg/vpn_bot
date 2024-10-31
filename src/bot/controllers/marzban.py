from datetime import UTC, datetime
import logging
from uuid import uuid4

from dateutil.relativedelta import relativedelta
import httpx
from pinkhash import PinkHash
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import settings
from bot.controllers.crud.user import update_db_user_expiration
from bot.internal.dicts import texts
from database.models import User

logger = logging.getLogger(__name__)


async def get_marzban_token() -> str:
    url = f"{settings.MARZBAN_BASE_URL}/api/admin/token"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "username": settings.MARZBAN_ADMIN,
        "password": settings.MARZBAN_PASS.get_secret_value(),
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get("access_token")


async def create_marzban_user(username: str, tg_id: int, token: str, duration: relativedelta) -> dict:
    url = f"{settings.MARZBAN_BASE_URL}/api/user"
    pink = PinkHash(language_name="eng1", option="en")
    expire_date = datetime.now(UTC) + duration
    expire_timestamp = int(expire_date.timestamp())
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = {
        "username": pink.convert(username).replace(" ", "_"),
        "expire": expire_timestamp,
        "note": f"Telegram user: {username}, tg_id: {tg_id}",
        "proxies": {"vmess": {"id": str(uuid4())}},
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        try:
            response.raise_for_status()
            logger.info(f"Server response: {response.json()}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.exception(f"Server response with error: {response.json()}, error: {e}")
            raise


async def get_marzban_user(username: str, token: str) -> dict:
    url = f"{settings.MARZBAN_BASE_URL}/api/user/{username}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        try:
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.exception(f"Server response with error: {response.json()}, error: {e}")
            raise


async def update_marzban_user_expiration(username: str, token: str, duration: relativedelta, user_expired_at: datetime) -> dict:
    url = f"{settings.MARZBAN_BASE_URL}/api/user/{username}"
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
            logger.info(f"Server response: {response.json()}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.exception(f"Server response with error: {response.json()}, error: {e}")
            raise


async def process_subscription(
    user: User, duration: relativedelta, current_timestamp: int, db_session: AsyncSession
) -> str:
    valid_until = await update_db_user_expiration(user, duration, db_session)
    days_left = (valid_until.timestamp() - current_timestamp) // (24 * 3600)
    expire_date_str = valid_until.strftime("%d.%m.%Y")
    return texts['renew_subscription'].format(
        added_time=get_duration_string(duration),
        status='Active',
        proxy_type='VMess',
        valid_until=expire_date_str,
        days_left=int(days_left),
    )


def get_duration_string(duration: relativedelta):
    match duration:
        case relativedelta(weeks=1):
            return "1 week"
        case relativedelta(months=1):
            return "1 month"
        case relativedelta(months=6):
            return "6 months"
        case relativedelta(years=1):
            return "1 year"
        case _:
            return "Unexpected duration"
