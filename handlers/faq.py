from aiogram import Router, F
from aiogram.types import CallbackQuery

from data import FAQ
from keyboards import faq_kb, back_to_faq_kb

router = Router()


@router.callback_query(F.data.startswith("faq:"))
async def show_faq_answer(callback: CallbackQuery):
    faq_id = callback.data.split(":")[1]
    question = next(q for q in FAQ if q["id"] == faq_id)

    text = f"<b>{question['q']}</b>\n\n{question['a']}"
    await callback.message.edit_text(text, reply_markup=back_to_faq_kb())
    await callback.answer()


@router.callback_query(F.data == "back:faq")
async def back_to_faq(callback: CallbackQuery):
    await callback.message.edit_text("Частые вопросы:", reply_markup=faq_kb())
    await callback.answer()
