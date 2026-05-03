from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup
from aiogram.types import Message,CallbackQuery,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
from forms.user import Form
from aiogram.fsm.context import FSMContext
router = Router()

@router.message(command="ne")
async def ne(message: Message, state: FSMContext):
    await message.answer("Анкета:Введите свое имя")
    await state.set_state(Form.name)
@router.message(command="cancel")
async def cancel_form(message: Message, state: FSMContext):
     await state.clear()
     await message.answer("Анкета отменена")
@router.message(Form.name, F.text)
async def procces_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Анкета:Введите свой возраст")
    await state.set_state(Form.age)
@router.message(Form.age, F.text)
async def procces_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должнен быть числом")
        return

    if int(message.text)<1 or int(message.text)>100:
        await message.answer("Возраст должен быть от 1 до 100")
        return

    await state.update_data(age=message.text)
    await message.answer("Анкета:Email введите ")
    await state.clear()
@router.message(Form.email, F.text)
async def procces_email(message: Message, state: FSMContext):
    email_text=message.text
    if "@" not in email_text or "." in email_text:
        await message.answer("Email не корректный")
        return
    await state.update_data(email=email_text)
    data = await state.get_data()
    name = data["name"]
    age = data["age"]
    email = data["email"]
    await message.answer(f"Все готово:{name},{age},{email}")





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