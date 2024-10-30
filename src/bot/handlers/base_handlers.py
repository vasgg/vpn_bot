from datetime import UTC, datetime

from aiogram import F, Router
from aiogram.filters import (
    CommandStart,
)
from aiogram.types import CallbackQuery, LabeledPrice, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.controllers.crud.link import get_links_by_user_id
from bot.internal.enums import SubscriptionPrice
from bot.internal.keyboards import (
    SubscriptionCallbackFactory,
    buy_subscription_kb,
    close_links_kb,
    connect_vpn_kb,
    show_links_kb,
)
from bot.internal.lexicon import texts
from bot.controllers.crud.user import get_user_from_db_by_tg_id

router = Router()


@router.message(CommandStart())
async def start(message: Message, db_session: AsyncSession) -> None:
    user = await get_user_from_db_by_tg_id(message.from_user.id, db_session)
    current_time = datetime.now(UTC)
    if not user:
        # await message.answer(
        #     texts['user_expired'].format(
        #         user_fullname=message.from_user.full_name,
        #         status='Inactive',
        #     ),
        #     reply_markup=connect_vpn_kb(),
        # )
        prices = [LabeledPrice(label="XTR", amount=SubscriptionPrice.ONE_WEEK_DEMO_ACCESS.value)]
        await message.answer_invoice(
            title="Demo access to VPN",
            description="For access to VPN, please purchase a subscription",
            payload="demo access",
            currency="XTR",
            prices=prices,
            start_parameter="stars-payment",
        )
    else:
        if user.expired_at > message.date:
            delta = user.expired_at - current_time
            formatted_date = user.expired_at.strftime("%d.%m.%Y")
            await message.answer(
                texts['start_message'].format(
                    user_fullname=message.from_user.full_name,
                    user_id=message.from_user.id,
                    status='Active',
                    proxy_type='VMess',
                    valid_until=formatted_date,
                    days_left=delta.days,
                ),
                reply_markup=show_links_kb(),
            )
        else:
            await message.answer(
                texts['user_expired'].format(
                    user_fullname=message.from_user.full_name,
                    status='Inactive',
                ),
                reply_markup=connect_vpn_kb(),
            )


@router.callback_query(SubscriptionCallbackFactory.filter())
async def subscription_prolongation(
    callback: CallbackQuery,
    callback_data: SubscriptionCallbackFactory,
) -> None:
    await callback.answer()
    match callback_data.stars_amount:
        case SubscriptionPrice.ONE_WEEK_DEMO_ACCESS:
            prices = [LabeledPrice(label="XTR", amount=SubscriptionPrice.ONE_WEEK_DEMO_ACCESS.value)]
            description = 'Access to VPN for 1 week'
        case SubscriptionPrice.ONE_MONTH_SUBSCRIPTION:
            prices = [LabeledPrice(label="XTR", amount=SubscriptionPrice.ONE_MONTH_SUBSCRIPTION.value)]
            description = 'Access to VPN for 1 month'
        case SubscriptionPrice.SIX_MONTH_SUBSCRIPTION:
            prices = [LabeledPrice(label="XTR", amount=SubscriptionPrice.SIX_MONTH_SUBSCRIPTION.value)]
            description = 'Access to VPN for 6 month'
        case SubscriptionPrice.ONE_YEAR_SUBSCRIPTION:
            prices = [LabeledPrice(label="XTR", amount=SubscriptionPrice.ONE_YEAR_SUBSCRIPTION.value)]
            description = 'Access to VPN for 12 month'
        case _:
            assert False, f'unexpected value {callback_data.stars_amount}'
    await callback.message.answer_invoice(
        title="Access to VPN",
        description=description,
        payload="payment for VPN",
        currency="XTR",
        prices=prices,
        start_parameter="stars-payment",
    )


@router.callback_query(F.data == 'show links')
async def show_links(callback: CallbackQuery, db_session: AsyncSession) -> None:
    await callback.answer()
    links = await get_links_by_user_id(callback.from_user.id, db_session)
    await callback.message.answer(
        texts['links_message'].format(links='\n\n'.join(i for i in links)), reply_markup=close_links_kb()
    )


@router.callback_query(F.data == 'close links')
async def close_links(callback: CallbackQuery) -> None:
    await callback.message.delete()


@router.callback_query(F.data == 'connect')
async def close_links(callback: CallbackQuery) -> None:
    await callback.answer()

    # await callback.message.answer_invoice(
    #     title="Connect to VPN",
    #     description="For access to VPN, please purchase a subscription",
    #     payload="VPN access",
    #     currency="XTR",
    #     prices=prices,
    #     start_parameter="stars-payment",
    #     reply_markup=buy_subscription_kb(demo_access_used),
    # )
    await callback.message.answer(
        texts['choose_action'],
        reply_markup=buy_subscription_kb(),
    )
