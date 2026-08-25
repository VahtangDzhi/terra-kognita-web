"""
Логика оформления заказа.

Это многошаговый диалог: бот задаёт вопрос -> ждёт ответ -> сохраняет его
в FSMContext (временное хранилище состояния конкретного пользователя) ->
задаёт следующий вопрос. В конце собираем все данные и отправляем заказ
админу.
"""

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from data import find_item
from keyboards import sizes_kb, confirm_order_kb, main_menu_kb
from states import OrderStates
from config import ADMIN_CHAT_ID

router = Router()


@router.callback_query(F.data.startswith("order:"))
async def start_order(callback: CallbackQuery, state: FSMContext):
    """Начало заказа: пользователь нажал 'Заказать' на карточке товара."""
    item_id = callback.data.split(":")[1]
    _, item = find_item(item_id)

    # Сохраняем id товара в состояние — он понадобится в самом конце
    await state.update_data(item_id=item_id)
    await state.set_state(OrderStates.waiting_size)

    await callback.message.edit_text(
        f"Отлично! Выбери размер для <b>{item['name']}</b>:",
        reply_markup=sizes_kb(item_id),
    )
    await callback.answer()


@router.callback_query(OrderStates.waiting_size, F.data.startswith("size:"))
async def process_size(callback: CallbackQuery, state: FSMContext):
    size = callback.data.split(":")[1]
    await state.update_data(size=size)
    await state.set_state(OrderStates.waiting_name)

    await callback.message.edit_text(
        f"Размер {size} выбран ✅\n\nКак тебя зовут? Напиши имя и фамилию."
    )
    await callback.answer()


@router.message(OrderStates.waiting_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(OrderStates.waiting_phone)
    await message.answer("Принято! Теперь напиши номер телефона для связи.")


@router.message(OrderStates.waiting_phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(OrderStates.waiting_city)
    await message.answer("Супер! В какой город отправлять заказ?")


@router.message(OrderStates.waiting_city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(OrderStates.confirm)

    data = await state.get_data()
    _, item = find_item(data["item_id"])

    summary = (
        "Проверь, всё верно? 👇\n\n"
        f"Товар: {item['name']}\n"
        f"Размер: {data['size']}\n"
        f"Цена: {item['price']}₽\n"
        f"Имя: {data['name']}\n"
        f"Телефон: {data['phone']}\n"
        f"Город: {data['city']}"
    )
    await message.answer(summary, reply_markup=confirm_order_kb())


@router.callback_query(OrderStates.confirm, F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    _, item = find_item(data["item_id"])

    # Сообщение пользователю
    await callback.message.edit_text(
        "Заказ принят! 🎉 Менеджер свяжется с тобой в течение дня для подтверждения."
    )
    await callback.message.answer("Что дальше?", reply_markup=main_menu_kb())

    # Уведомление админу — самое важное для реального бизнеса
    admin_text = (
        "🆕 <b>Новый заказ!</b>\n\n"
        f"Товар: {item['name']}\n"
        f"Размер: {data['size']}\n"
        f"Цена: {item['price']}₽\n"
        f"Имя: {data['name']}\n"
        f"Телефон: {data['phone']}\n"
        f"Город: {data['city']}\n"
        f"От пользователя: @{callback.from_user.username or callback.from_user.id}"
    )
    await bot.send_message(ADMIN_CHAT_ID, admin_text)

    await state.clear()
    await callback.answer()


@router.callback_query(OrderStates.confirm, F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Заказ отменён. Если что — каталог всегда открыт в меню 👇")
    await callback.message.answer("Главное меню:", reply_markup=main_menu_kb())
    await callback.answer()
