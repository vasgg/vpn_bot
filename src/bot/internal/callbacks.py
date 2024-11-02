from aiogram.filters.callback_data import CallbackData

from bot.internal.enums import DeviceType, MenuAction, SubscriptionPlan


class SubscriptionCallbackFactory(CallbackData, prefix='subscription'):
    plan: SubscriptionPlan


class MenuCallbackFactory(CallbackData, prefix='menu'):
    action: MenuAction


class DeviceCallbackFactory(CallbackData, prefix='device'):
    option: DeviceType
