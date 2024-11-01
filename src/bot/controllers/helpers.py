from aiogram.types import Message
from dateutil.relativedelta import relativedelta
from pinkhash import PinkHash


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


def compose_username(message: Message):
    return (
        '@' + message.from_user.username
        if message.from_user.username
        else message.from_user.full_name.replace(' ', '_')
    )
