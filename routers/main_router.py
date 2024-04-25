from aiogram import Router
from routers.commands.registration import router as registration_router
from routers.commands.common_commands import router as common_commands_router
from routers.commands.search_user_commands import router as search_user_router

router = Router()
router.include_router(registration_router)
router.include_router(search_user_router)
router.include_router(common_commands_router)