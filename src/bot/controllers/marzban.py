from asyncio import sleep
from datetime import UTC, datetime
import logging
from uuid import uuid4

from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from dateutil.relativedelta import relativedelta
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import Settings
from bot.controllers.crud.link import update_links_url
from bot.internal.helpers import pink_convert
from database.models import User

logger = logging.getLogger(__name__)


class MarzbanClient:
    def __init__(
        self,
        settings: Settings,
    ):
        self.base_url = settings.marzban.BASE_URL
        self.username = settings.marzban.ADMIN
        self.password = settings.marzban.PASSWORD.get_secret_value()
        self.client = httpx.AsyncClient()  # тут без контекстного менеджера создаём, значит ли это, что надо
        #  будет везде явно закрывать клиент?
        self.token = None
        self.headers_with_token = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    async def init_token(self):
        async with httpx.AsyncClient() as client:  # может это тоже надо заменить на общий вызов process_request?
            headers = {
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            data = {
                "username": self.username,
                "password": self.password,
            }
            response = await client.post(self.base_url, headers=headers, data=data)
            try:
                response.raise_for_status()
                logger.info(f"Obtaining Marzban token. Server response: {response.json()}")
                token_data = response.json()
                self.token = token_data.get("access_token")
            except httpx.HTTPStatusError as e:
                logger.exception(f"Obtaining Marzban token. Server response with error: {response.json()}, error: {e}")
                raise
            # мы сделали перевыпуск токена только в том случае, когда токена нет сразу, либо при ошибке с получением
            # но что будет, если вылезет ошибка токена в других методах? отыграет как надо перевыпуск нового?
            # не достаточно понимаю, как работает, но сомневаюсь, что отыграет

    async def process_request(
        self,
        method,
        url: str,
        headers: dict,
        data: dict | None = None,
        json: dict | None = None,
    ) -> dict:
        url = self.base_url + url
        response = await method(url, headers=headers, json=json, data=data)
        try:
            response.raise_for_status()
            logger.info(f"Creating new Marzban user. Server response: {response.json()}")
            return response.json()
        except httpx.HTTPStatusError:
            await self.init_token()
            try:
                response = await method(self.base_url, headers=headers, json=json, data=data)
                response.raise_for_status()
                logger.info(f"Calling Marzban API with {method}. Server response: {response.json()}")
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.exception(f"Calling Marzban API with {method}. "
                                 f"Server response with error: {response.json()}, error: {e}")
                raise

    async def create_marzban_user(
        self,
        username: str,
        tg_id: int,
        duration: relativedelta | None = None,
        expire: datetime | None = None
    ):
        if duration:
            expire_date = datetime.now(UTC) + duration
            expire_timestamp = int(expire_date.timestamp())
        else:
            expire_timestamp = int(expire.timestamp())
        json = {
            "username": pink_convert(username),
            "expire": expire_timestamp,
            "note": f"Telegram user: {username}, tg_id: {tg_id}",
            "proxies": {"vmess": {"id": str(uuid4())}},
        }
        await self.process_request(httpx.post, "/api/user", headers=self.headers_with_token, json=json)

    async def delete_marzban_user(self, username: str):
        url = f"{self.base_url}/api/user/{username}"
        await self.process_request(httpx.delete, url, headers=self.headers_with_token)

    async def update_marzban_user_expiration(
        self,
        username: str,
        duration: relativedelta,
        user_expired_at: datetime,
    ):
        url = f"{self.base_url}/api/user/{username}"
        now = datetime.now(UTC)
        if user_expired_at.tzinfo is None:
            user_expired_at = user_expired_at.replace(tzinfo=UTC)
        if user_expired_at < now:
            expire_date = now + duration
            expire_timestamp = int(expire_date.timestamp())
        else:
            expire_date = user_expired_at + duration
            expire_timestamp = int(expire_date.timestamp())
        json = {"expire": expire_timestamp}
        await self.process_request(httpx.put, url, headers=self.headers_with_token, json=json)

    async def renew_links(
        self,
        message: Message,
        user: User,
        db_session: AsyncSession
    ):
        # вот тут уже нужна помощь.
        # может, этот метод и не надо в класс заносить?
        # а с другой стороны, схуяли бы нет?
        # токен у нас теперь автоматом создаётся при колле класса?
        ...


async def renew_links(message: Message, user: User, settings: Settings, db_session: AsyncSession):
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.from_user.id):
        marzban_token = await get_marzban_token(settings=settings)
        await delete_marzban_user(user.marzban_username, marzban_token)
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
