from datetime import UTC
from math import ceil, floor

from aiogram.types import User, Message
from dateutil.relativedelta import relativedelta
from pinkhash import PinkHash

from bot.internal.dicts import texts
from bot.internal.enums import SubscriptionStatus
from database.models import User as DBUser


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


def pink_convert(text: str) -> str:
    pink = PinkHash(language_name="eng1", option="en")
    return pink.convert(text).replace(" ", "_")


def compose_username(user: User):
    return '@' + user.username if user.username else user.full_name.replace(' ', '_')


def compose_message(user: DBUser, message: Message, status: SubscriptionStatus) -> str:

    if status == SubscriptionStatus.INACTIVE or user.expired_at is None:
        return texts[SubscriptionStatus.INACTIVE].format(
            user_id=message.from_user.id,
        )
    days_left_float = (user.expired_at.replace(tzinfo=UTC) - message.date.replace(tzinfo=UTC)).total_seconds() / (
        24 * 3600
    )
    days_left = ceil(days_left_float) if days_left_float > floor(days_left_float) + 0.8 else floor(days_left_float)

    return texts[status].format(
        user_id=user.tg_id, valid_until=user.expired_at.strftime("%d.%m.%Y"), days_left=days_left
    )
