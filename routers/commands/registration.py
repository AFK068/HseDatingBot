from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F, Router
import data_base.requests
import handle_user_input
from states import Form
import keyboards

router = Router()


@router.message(F.text == "Зарегестрироваться")
async def handle_registration(message: Message, state: FSMContext):
    if await data_base.requests.check_user_exists(message.from_user.id):
        await state.set_state(Form.split_registration)
        await message.answer("Вы уже зарегистрированы",
                             reply_markup=keyboards.user_telegram_id_repeated_registration_keyboard)
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
        await state.set_state(Form.register_faculty)
        await message.answer("Введи свой факультет", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Нет такого варианта ответа")


@router.message(Form.register_faculty)
async def registration_user_faculty(message: Message, state: FSMContext):
    await state.update_data(register_faculty=message.text)
    data = await state.get_data()

    if await handle_user_input.check_faculty_existance(data["register_faculty"]):
        await state.set_state(Form.register_photo)
        await message.answer("Теперь давай добавим фото (не более 3)", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Нет такого варианта ответа")


@router.message(Form.register_photo, F.photo)
async def handle_user_photo(message: Message, state: FSMContext):
    data = await state.get_data()

    if 'register_photo' in data:
        if len(data['register_photo']) < 3:
            data['register_photo'].append(message.photo[-1].file_id)
        else:
            await message.answer("Вы отправили более 3 фотографий, добавлены будут только первые 3")
            await register_photo_process(message, state)
            return
    else:
        await state.update_data(register_photo=[message.photo[-1].file_id])

    end_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Всё")]], resize_keyboard=True,
                                       one_time_keyboard=True)
    await message.answer("Фотография добавлена", reply_markup=end_keyboard)


@router.message(Form.register_photo)
async def register_photo_process(message: Message, state: FSMContext):
    data = await state.get_data()
    if 'register_photo' in data:
        if message.text == "Всё":
            await state.set_state(Form.register_description)
            await message.answer("Расскажи о себе")
        else:
            await message.answer('Чтобы продолжить введите "Всё"')
    else:
        await message.answer("Вы должны отправить хотя бы одно фото")


@router.message(Form.register_description)
async def registration_user_in_database(message: Message, state: FSMContext):
    await state.update_data(register_description=message.text)
    data = await state.get_data()

    photos_str = ";".join(photo for photo in data["register_photo"])

    await data_base.requests.set_user(message.from_user.id, message.chat.id, data["register_name"],
                                      data["register_age"], data["register_gender"],
                                      data["register_gender_search"], data["register_faculty"],
                                      photos_str, data["register_description"])

    await message.answer("Данные успешно сохранены", reply_markup=keyboards.start_main_keyboard)
    await state.clear()
