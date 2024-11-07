from aiogram.filters.callback_data import CallbackData

from bot.internal.enums import DeviceType, HelpMenuAction, MainMenuAction, SubscriptionPlan


class SubscriptionCallbackFactory(CallbackData, prefix='subscription'):
    plan: SubscriptionPlan


class MenuCallbackFactory(CallbackData, prefix='menu'):
    action: MainMenuAction


class HelpCallbackFactory(CallbackData, prefix='help'):
    action: HelpMenuAction


class DeviceCallbackFactory(CallbackData, prefix='device'):
    option: DeviceType
