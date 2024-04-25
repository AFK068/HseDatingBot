from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    document = State()
    message = State()
    split_registration = State()
    register_name = State()
    register_age = State()
    register_gender = State()
    register_gender_search = State()
    register_faculty = State()
    register_photo = State()
    register_description = State()
    split_search_user_or_rewrite_data = State()
    search_user = State()
