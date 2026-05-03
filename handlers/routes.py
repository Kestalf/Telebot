from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message,CallbackQuery,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
router = Router()

def get_main_reply_keyboard():
    keyboard= ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="О боте")],
            [KeyboardButton(text="Старт"), KeyboardButton(text="Помощь")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_main_inline_keyboard():
    keyboard= InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть сайт",url="www.google.com")],
            [InlineKeyboardButton(text="Подробнее",callback_data="info_more")]
        ]
    )
    return keyboard

@router.callback_query(lambda c: c.data == "info_more")
async def process_more(callback: CallbackQuery):
    await callback.message.answer("Вот более подробная информация")
    await callback.answer()
@router.message(Command("start"))
@router.message(F.text.lower() == "старт")
async def start(message: Message):
    await message.answer("Привет")

@router.message(Command("help"))
async def help(message: Message):
    await message.answer("команды\n"
                         "/start\n"
                         "/about\n"
                         "/help",reply_markup=get_main_reply_keyboard())

@router.message(Command("about"))
async def about(message: Message):
    await message.answer(f"Привет,{message.from_user.first_name}",reply_markup=get_main_inline_keyboard())