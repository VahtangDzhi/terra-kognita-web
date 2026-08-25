from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from keyboards import main_menu_kb, categories_kb, faq_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Срабатывает на команду /start — первое сообщение от пользователя."""
    text = (
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Это бот <b>StreetWear Hub</b> — здесь можно посмотреть каталог "
        "и оформить заказ прямо в чате, без переходов на сайт.\n\n"
        "Выбирай раздел внизу 👇"
    )
    await message.answer(text, reply_markup=main_menu_kb())


@router.message(F.text == "🛍 Каталог")
async def open_catalog(message: Message):
    await message.answer("Выбери категорию:", reply_markup=categories_kb())


@router.message(F.text == "❓ FAQ")
async def open_faq(message: Message):
    await message.answer("Частые вопросы:", reply_markup=faq_kb())


@router.message(F.text == "✉️ Связаться с менеджером")
async def contact_manager(message: Message):
    await message.answer(
        "Можешь написать свой вопрос прямо сюда — менеджер ответит в течение дня.\n"
        "Либо напиши нам напрямую: @your_manager_username"
    )
