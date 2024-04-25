async def check_user_name_for_correctness(input_string):
    return all(char.isalpha() for char in input_string)


async def check_user_age_for_correctness(input_string):
    if input_string.lstrip('-').isdigit():
        return int(input_string) > 0, "Возраст корректен" if int(input_string) > 0 else "Введите положительное число"
    else:
        return False, "Введите число, а не текст"


async def check_user_gender_for_correctness(input_string):
    return input_string in ['Я парень', 'Я девушка']


async def check_user_gender_search_for_correctness(input_string):
    return input_string in ['Девушки', 'Парни', 'Все равно']


async def check_slit_registration_for_correctness(input_string):
    return input_string in ['Посмотреть мою анкету', 'Заполнить анкету заново', 'Вернуться назад']


async def check_faculty_existance(input_string):
    return True