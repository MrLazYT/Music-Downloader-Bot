from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

keyboard = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton("Скачати пісню за назвою")
        ],
        [
            KeyboardButton("Скачати пісню за посиланням (НЕ ДОСТУПНО!)")
        ],
        [
            KeyboardButton("Скачати усі пісні з плейлисту (БЕТА)")
        ],
        [
            KeyboardButton("Інформація")
        ]
    ],
    resize_keyboard = True,
    one_time_keyboard = True
)

beta_keyboard = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton("Так"),
            KeyboardButton("Ні")
        ],
    ],
    resize_keyboard = True,
    one_time_keyboard = True
)

info_keyboard = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton("Інформація про всі версії")
        ]
    ],
    resize_keyboard = True,
    one_time_keyboard = True
)