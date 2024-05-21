import data_base.requests
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types.input_media_photo import InputMediaPhoto


async def output_user(message: Message, state: FSMContext, user):
    photo_ids = user.photo.split(";")

    media = [InputMediaPhoto(media=photo_ids[0], caption=f'{user.name}, {user.age}\nКого ищу: {user.search_gender}\n'
                                                         f'Факультет: {user.faculty}\nОбо мне: {user.description}')]

    for photo_id in photo_ids[1:]:
        media.append(InputMediaPhoto(media=photo_id))

    await message.answer_media_group(media=media)


async def search_and_output_random_user(message: Message, state: FSMContext):
    user = await split_search_user_by_search_gender(message, state)

    if user is None:
        return None

    await output_user(message, state, user)
    return user


async def split_search_user_by_search_gender(message: Message, state: FSMContext):
    current_user = await data_base.requests.get_user_by_telegram_id(message.from_user.id)

    if current_user.search_gender == "Девушки":
        return await data_base.requests.get_random_user_with_search_gender("Я девушка")

    elif current_user.search_gender == "Парни":
        return await data_base.requests.get_random_user_with_search_gender("Я парень")

    elif current_user.search_gender == "Все равно":
        return await data_base.requests.get_user_by_telegram_id(await data_base.requests.get_random_user_telegram_id())