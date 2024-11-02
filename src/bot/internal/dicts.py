# fmt: off
from dateutil.relativedelta import relativedelta

from bot.internal.enums import SubscriptionPlan

texts = {
    'inactive': 'VPN bot.\n\n'
                'User ID: <code>{user_id}</code>\n'
                '└ your status: <b>Inactive</b>\n',
    'active': 'VPN bot.\n\n'
              'User ID: <code>{user_id}</code>\n'
              '├ your status: <b>Active</b>\n'
              '├ proxy type: <b>VMess</b>\n'
              '├ valid until: <b>{valid_until}</b>\n'
              '└ days left: <b>{days_left}</b>\n\n',
    'created': 'You have been successfully registered.\n\n'
               'User ID: <code>{user_id}</code>\n'
               '├ your status: <b>Active</b>\n'
               '├ proxy type: <b>VMess</b>\n'
               '├ valid until: <b>{valid_until}</b>\n'
               '└ days left: <b>{days_left}</b>\n\n',
    'renewed': 'Renewed your subscription.\n\n'
               'User ID: <code>{user_id}</code>\n'
               '├ your status: <b>Active</b>\n'
               '├ proxy type: <b>VMess</b>\n'
               '├ valid until: <b>{valid_until}</b>\n'
               '└ days left: <b>{days_left}</b>\n\n',
    'prolonged': 'Your subscription successfully prolonged.\n\n'
                 'User ID: <code>{user_id}</code>\n'
                 '├ your status: <b>Active</b>\n'
                 '├ proxy type: <b>VMess</b>\n'
                 '├ valid until: <b>{valid_until}</b>\n'
                 '└ days left: <b>{days_left}</b>\n\n',
    'choose_action': 'Add more time to your subscription.',
    'choose_device': 'Choose a device:',
    'links_message': '<pre>{links}</pre>',
    'links_refreshed': 'Links successfully refreshed.',
}

goods = {
    SubscriptionPlan.ONE_WEEK_DEMO_ACCESS: {
        "price": 1,
        "duration": relativedelta(weeks=1),
    },
    SubscriptionPlan.ONE_MONTH_SUBSCRIPTION: {
        "price": 10,
        "duration": relativedelta(months=1),
    },
    SubscriptionPlan.SIX_MONTH_SUBSCRIPTION: {
        "price": 20,
        "duration": relativedelta(months=6),
    },
    SubscriptionPlan.ONE_YEAR_SUBSCRIPTION: {
        "price": 30,
        "duration": relativedelta(years=1),
    },
}
# fmt: on
