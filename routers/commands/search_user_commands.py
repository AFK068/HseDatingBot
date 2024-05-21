from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import keyboards
import data_base.requests
import logic_search_users
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.filters.state import StateFilter

from states import Form

router = Router()


@router.message(F.text == "Начать поиск", ~StateFilter(Form))
async def handle_user_search(message: Message, state: FSMContext):
    if not await data_base.requests.check_user_exists(message.from_user.id):
        await message.answer("Для начала зарегестрируйтесь")
        return

    await message.answer("Перед началом давай взглянем на твою анкету:", reply_markup=keyboards.start_search_user_keyboard)
    user = await data_base.requests.get_user_by_telegram_id(message.from_user.id)

    await logic_search_users.output_user(message, state, user)
    await state.set_state(Form.split_search_user_or_rewrite_data)


@router.message(Form.split_search_user_or_rewrite_data)
async def split_search_user_or_rewrite_data(message: Message, state: FSMContext):
    await state.update_data(split_search_user_or_rewrite_data=message.text)
    data = await state.get_data()

    if data["split_search_user_or_rewrite_data"] == "Начать поиск":
        await state.set_state(Form.search_user)
        await search_user(message, state)
        return

    elif data["split_search_user_or_rewrite_data"] == "Заполнить анкету заново":
        await state.set_state(Form.register_name)
        await message.answer("Введите свое имя", reply_markup=ReplyKeyboardRemove())

    else:
        await message.answer("Нет такого варианта ответа")


@router.message(Form.search_user)
async def search_user(message: Message, state: FSMContext):
    await state.update_data(search_user=message.text)
    data = await state.get_data()

    if data["search_user"] == "💤":
        await message.answer("Подождем пока кто-то заинтересуется твоей анкетой", reply_markup=keyboards.start_main_keyboard)

    # поменять клаву если кто-то лайкнул
    await message.answer(text="✨🔍", reply_markup=keyboards.user_main_search_keyboard)

    user = await logic_search_users.search_and_output_random_user(message, state)

    if user is None:
        await message.answer("Похоже, нет никого для поиска(")
        return

    if data["search_user"] == "🤍":
        print(1)
    elif data["search_user"] == "👎":
        print(2)
    elif data["search_user"] == "Начать поиск":
        pass
    else:
        await message.answer("Нет такого варианта ответа")