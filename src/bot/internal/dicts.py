# fmt: off
from dateutil.relativedelta import relativedelta

from bot.internal.enums import SubscriptionPlan

texts = {
    'welcome': 'Greetings, {username} 👋\n\n'
               'Here you can connect to a secure and fast internet without geographical restrictions!\n\n'
               'By choosing us, you get:\n\n'
               '🔐 Personal data privacy\n\n'
               '🚀 High speed and unlimited traffic.',
    'inactive': 'Mega VPN.\n\n'
                'User ID: <code>{user_id}</code>\n'
                '└ your status: <b>Inactive</b>\n',
    'active': 'Mega VPN.\n\n'
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
    'help': 'Mega VPN bot help.\n\n'
            'User ID: <code>{user_id}</code>\n',
    'stars': 'Stars can be acquired through in-app purchases via Apple and Google or PremiumBot, '
             'then spent on digital products offered by bots – from e-books '
             'and online courses to items in Telegram games.',
    'vpn_not_working': 'If your VPN is not working, please check/try the following:\n\n'
                       '👉 Make sure that the links are set up in the app for connecting to the VPN. Use the "📱 Setup device" button.\n'
                       '👉 Check if your status is active ("🚀 Buy access" button).\n'
                       '👉 Update the VPN app.\n'
                       '👉 Restart your phone.\n'
                       '👉 Ensure that other VPN services are removed in your phone’s settings!',
    'low_speed': 'We carefully monitor the connection status to our servers.\n'
                 'In 90% of cases, slow speeds are caused by the end internet provider / connection quality.'
                 'If none of the servers provide you with high speed, please refer to the "VPN not working" help section.',
    'choose_plan': 'Add more time to your access.',
    'choose_device': 'Choose a device:',
    'demo_used': 'You have already used a demo access.',
    'links_message': '<pre>{links}</pre>',
    'links_refreshed': 'Links successfully refreshed.',
    'support': 'You can contact support by sending a message to @honeybadger367',
}

goods = {
    SubscriptionPlan.ONE_WEEK_DEMO_ACCESS: {
        "price": 1,
        "duration": relativedelta(weeks=1),
    },
    SubscriptionPlan.ONE_MONTH_SUBSCRIPTION: {
        "price": 150,
        "duration": relativedelta(months=1),
    },
    SubscriptionPlan.SIX_MONTH_SUBSCRIPTION: {
        "price": 700,
        "duration": relativedelta(months=6),
    },
    SubscriptionPlan.ONE_YEAR_SUBSCRIPTION: {
        "price": 1200,
        "duration": relativedelta(years=1),
    },
}
# fmt: on
