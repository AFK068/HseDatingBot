from data_base.models import async_session
from data_base.models import User
from sqlalchemy import select, update, delete
import random


async def set_user(tg_id, user_chat_id, user_name, user_age, user_gender, user_search_gender, user_description):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == tg_id))

        if user:
            user.name = user_name
            user.age = user_age
            user.gender = user_gender
            user.search_gender = user_search_gender
            user.description = user_description
        else:
            new_user = User(telegram_id=tg_id, chat_id=user_chat_id, name=user_name, age=user_age, gender=user_gender,
                            search_gender=user_search_gender, description=user_description)
            session.add(new_user)

        await session.commit()


async def check_user_exists(telegram_id: int) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        return user is not None


async def get_user_by_telegram_id(telegram_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalars().first()
        return user


async def get_random_user_telegram_id():
    async with async_session() as session:
        result = await session.execute(select(User.telegram_id))
        telegram_ids = [row for row in result.scalars()]
        if telegram_ids:
            random_telegram_id = random.choice(telegram_ids)
            return random_telegram_id
        else:
            return None


async def get_random_user_with_search_gender(gender):
    async with async_session() as session:
        result = await session.execute(
            select(User).filter(User.search_gender == gender)
        )
        users = [row[0] for row in result]
        if users:
            random_user = random.choice(users)
            return random_user
        else:
            return None