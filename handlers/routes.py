from aiogram import Router
router = Router()

@router.message()
async def hello(message):
    await message.answer("Hello World!")