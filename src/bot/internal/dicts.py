# fmt: off
from dateutil.relativedelta import relativedelta

from bot.internal.enums import SubscriptionPlan

texts = {
    'no_subscription': 'Hello, {user_fullname}.\n\n'
                       'User ID: <code>{user_id}</code>\n'
                       '└ your status: <b>Inactive</b>\n',
    'start_message': 'Hello, {user_fullname}.\n\nUser ID: <code>{user_id}</code>\n'
                     '├ your status: <b>{status}</b>\n'
                     '├ proxy type: <b>{proxy_type}</b>\n'
                     '├ valid until: <b>{valid_until}</b>\n'
                     '└ days left: <b>{days_left}</b>\n\n',
    'user_created': 'You have been successfully registered, {user_fullname}.\n\n'
                    'User ID: <code>{user_id}</code>\n'
                    '├ your status: <b>Active</b>\n'
                    '├ proxy type: <b>{proxy_type}</b>\n'
                    '├ valid until: <b>{valid_until}</b>\n'
                    '└ days left: <b>{days_left}</b>\n\n',
    'links_message': '<pre>{links}</pre>',
    'user_not_expired': 'Hello, {user_fullname}.\n\n'
                        'User ID: <code>{user_id}</code>\n'
                        '├ your status: <b>Active</b>\n'
                        '├ proxy type: <b>{proxy_type}</b>\n'
                        '├ valid until: <b>{valid_until}</b>\n'
                        '└ days left: <b>{days_left}</b>\n\n',
    'renew_subscription': 'Reactivating your subscription by addind {added_time}.\n\n'
                          'User ID: <code>{user_id}</code>\n'
                          '├ your status: <b>Active</b>\n'
                          '├ proxy type: <b>{proxy_type}</b>\n'
                          '├ valid until: <b>{valid_until}</b>\n'
                          '└ days left: <b>{days_left}</b>\n\n',
    'prolong_subscription': 'Successfully added {added_time} to your subscription.\n\n'
                            'User ID: <code>{user_id}</code>\n'
                            '├ your status: <b>Active</b>\n'
                            '├ proxy type: <b>{proxy_type}</b>\n'
                            '├ valid until: <b>{valid_until}</b>\n'
                            '└ days left: <b>{days_left}</b>\n\n',
    'choose_action': 'Choose an option:',
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
