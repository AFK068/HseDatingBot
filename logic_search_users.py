import data_base.requests
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards import user_main_search_keyboard


async def search_and_output_random_user(message: Message, state: FSMContext):
    user = await split_search_user_by_search_gender(message, state)
    await message.answer(f"{user.name}, {user.age}\nКого ишу: {user.search_gender}\nОбо мне: {user.description}", reply_markup=user_main_search_keyboard)
    return user


async def split_search_user_by_search_gender(message: Message, state: FSMContext):
    current_user = await data_base.requests.get_user_by_telegram_id(message.from_user.id)

    if current_user.search_gender == "Девушки":
        return await data_base.requests.get_random_user_with_search_gender("Я девушка")

    elif current_user.search_gender == "Парни":
        return await data_base.requests.get_random_user_with_search_gender("Я парень")

    elif current_user.search_gender == "Все равно":
        return await data_base.requests.get_user_by_telegram_id(await data_base.requests.get_random_user_telegram_id())