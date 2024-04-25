from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_main_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="/help"),
                                                     KeyboardButton(text="Начать поиск")],
                                                    [KeyboardButton(text="Зарегестрироваться")],
                                                    [KeyboardButton(text="Правила использования")]], resize_keyboard=True)

user_gender_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Я парень"), KeyboardButton(text="Я девушка")]], resize_keyboard=True)

user_search_gender_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Девушки"),
                                                        KeyboardButton(text="Парни"),
                                                        KeyboardButton(text="Все равно")]], resize_keyboard=True)

user_telegram_id_repeated_registration_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Посмотреть мою анкету")],
                                                                                [KeyboardButton(text="Заполнить анкету заново")],
                                                                                [KeyboardButton(text="Вернуться назад")]], resize_keyboard=True)

user_main_search_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🤍"), KeyboardButton(text="👎"), KeyboardButton(text="🔙")]], resize_keyboard=True)

start_search_user_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Начать поиск"), KeyboardButton(text="Заполнить анкету заново")]], resize_keyboard=True)
