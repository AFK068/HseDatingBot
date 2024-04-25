from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import data_base.requests
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandStart
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
import keyboards
import handle_user_input
from aiogram.filters.state import StateFilter

from states import Form

router = Router()


@router.message(F.text == "Зарегестрироваться")
async def handle_registration(message: Message, state: FSMContext):
    if await data_base.requests.check_user_exists(message.from_user.id):
        await state.set_state(Form.split_registration)
        await message.answer("Вы уже зарегистрированы", reply_markup=keyboards.user_telegram_id_repeated_registration_keyboard)
    else:
        await state.set_state(Form.register_name)
        await message.answer("Введите свое имя", reply_markup=ReplyKeyboardRemove())


@router.message(Form.split_registration)
async def split_registration_user(message: Message, state: FSMContext):
    await state.update_data(split_registration=message.text)
    data = await state.get_data()

    if data["split_registration"] == "Посмотреть мою анкету":
        user = await data_base.requests.get_user_by_telegram_id(message.from_user.id)
        await message.answer(f"{user.name}, {user.age}\nКого ишу: {user.search_gender}\nОбо мне: {user.description}")
        return

    elif data["split_registration"] == "Заполнить анкету заново":
        await state.set_state(Form.register_name)
        await message.answer("Введите свое имя", reply_markup=ReplyKeyboardRemove())
        return

    elif data["split_registration"] == "Вернуться назад":
        await message.answer("◀️", reply_markup=keyboards.start_main_keyboard)
        await state.clear()
        return

    else:
        await message.answer("Нет такого варианта ответа")


@router.message(Form.register_name)
async def registration_user_name(message: Message, state: FSMContext):
    await state.update_data(register_name=message.text)
    data = await state.get_data()

    if await handle_user_input.check_user_name_for_correctness(data["register_name"]):
        await state.set_state(Form.register_age)
        await message.answer(f'Приятно познакомиться {data["register_name"]}, теперь введи свой возраст')
    else:
        await message.answer("Имя может содержать только буквы, попробуйте еще раз")


@router.message(Form.register_age)
async def registration_user_age(message: Message, state: FSMContext):
    await state.update_data(register_age=message.text)
    data = await state.get_data()

    is_correct, error_message = await handle_user_input.check_user_age_for_correctness(data["register_age"])
    if is_correct:
        await state.set_state(Form.register_gender)
        await message.answer("Отлично, теперь выбери свой пол", reply_markup=keyboards.user_gender_keyboard)
    else:
        await message.answer(error_message)


@router.message(Form.register_gender)
async def registration_user_gender(message: Message, state: FSMContext):
    await state.update_data(register_gender=message.text)
    data = await state.get_data()

    if await handle_user_input.check_user_gender_for_correctness(data["register_gender"]):
        await state.set_state(Form.register_gender_search)
        await message.answer("Кого ты хочешь искать", reply_markup=keyboards.user_search_gender_keyboard)
    else:
        await message.answer("Нет такого варианта ответа")


@router.message(Form.register_gender_search)
async def registration_user_gender_search(message: Message, state: FSMContext):
    await state.update_data(register_gender_search=message.text)
    data = await state.get_data()

    if await handle_user_input.check_user_gender_search_for_correctness(data["register_gender_search"]):
        await state.set_state(Form.register_description)
        await message.answer("Расскажи о себе", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Нет такого варианта ответа")


@router.message(Form.register_description)
async def registration_user_in_database(message: Message, state: FSMContext):
    await state.update_data(register_description=message.text)
    data = await state.get_data()

    await data_base.requests.set_user(message.from_user.id, message.chat.id, data["register_name"],
                                     data["register_age"], data["register_gender"],
                                     data["register_gender_search"], data["register_description"])

    await message.answer("Данные успешно сохранены", reply_markup=keyboards.start_main_keyboard)
    await state.clear()