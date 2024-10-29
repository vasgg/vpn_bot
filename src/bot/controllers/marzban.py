from datetime import datetime, timedelta
import logging
from uuid import uuid4

import httpx
from pinkhash import PinkHash

from bot.config import settings
from bot.controllers.crud.user import update_user_expiration
from bot.internal.lexicon import texts

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


async def create_marzban_user(username: str, tg_id: int, token: str, expire_after_weeks: int = 1) -> dict:
    url = f"{settings.MARZBAN_BASE_URL}/api/user"
    pink = PinkHash(language_name="eng1", option="en")
    expire_date = datetime.now() + timedelta(weeks=expire_after_weeks)
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


async def process_subscription(user, months, current_timestamp, db_session):
    valid_until = await update_user_expiration(user, months, db_session)
    days_left = (valid_until.timestamp() - current_timestamp) // (24 * 3600)
    expire_date_str = valid_until.strftime("%d.%m.%Y")
    return texts['renew_subscription'].format(
        month_amount=months,
        status='Active',
        proxy_type='VMess',
        valid_until=expire_date_str,
        days_left=int(days_left),
    )
