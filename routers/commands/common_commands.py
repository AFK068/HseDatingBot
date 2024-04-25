from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
import keyboards

from states import Form

router = Router()


# Command commands like: /start ; /help
@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Я телеграм бот, для знакомаств.", reply_markup=keyboards.start_main_keyboard)


@router.message(Command('help'))
async def handle_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Для начала нужно зарегистрироваться.")
