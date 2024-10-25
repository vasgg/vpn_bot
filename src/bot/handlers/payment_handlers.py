from aiogram import Bot, F, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject

from bot.internal.keyboards import demo_access_kb
from bot.internal.lexicon import texts

router = Router()


@router.callback_query(F.data == "subscription")
async def payment_handler(callback: types.CallbackQuery):
    await callback.answer()
    prices = [types.LabeledPrice(label="XTR", amount=1)]
    await callback.message.answer_invoice(
        title="Access to subscription",
        description="",
        payload="stars_payment_payload",
        currency="XTR",
        prices=prices,
        start_parameter="stars-payment"
    )


@router.pre_checkout_query()
async def on_pre_checkout_query(
    pre_checkout_query: types.PreCheckoutQuery,
):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def on_successful_payment(
    message: types.Message,
):
    await message.answer(
        f"payment successful!\n\ncharge_id: <code>{message.successful_payment.telegram_payment_charge_id}</code>",
        message_effect_id="5104841245755180586",
    )


@router.message(Command("refund"))
async def cmd_refund(
    message: types.Message,
    bot: Bot,
    command: CommandObject,
):
    transaction_id = command.args
    if transaction_id is None:
        await message.answer(
            "no refund code provided")
        return
    try:
        await bot.refund_star_payment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=transaction_id
        )
        await message.answer("refund successful", message_effect_id='5046589136895476101')
    except TelegramBadRequest as error:
        if "CHARGE_NOT_FOUND" in error.message:
            text = "refund code not found"
        elif "CHARGE_ALREADY_REFUNDED" in error.message:
            text = "refund already refunded"
        else:
            text = "refund code not found"
        await message.answer(text)
        return
