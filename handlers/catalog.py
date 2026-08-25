from aiogram import Router, F
from aiogram.types import CallbackQuery

from data import CATALOG, find_item
from keyboards import categories_kb, items_kb, item_detail_kb

router = Router()


@router.callback_query(F.data.startswith("cat:"))
async def show_category(callback: CallbackQuery):
    """Показывает список товаров в выбранной категории."""
    cat_key = callback.data.split(":")[1]
    cat = CATALOG[cat_key]
    await callback.message.edit_text(
        f"<b>{cat['title']}</b>\nВыбери товар:",
        reply_markup=items_kb(cat_key),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("item:"))
async def show_item(callback: CallbackQuery):
    """Показывает карточку конкретного товара."""
    item_id = callback.data.split(":")[1]
    cat_key, item = find_item(item_id)

    text = (
        f"<b>{item['name']}</b>\n"
        f"Цена: {item['price']}₽\n"
        f"Размеры: {', '.join(item['sizes'])}\n\n"
        f"{item['desc']}"
    )
    await callback.message.edit_text(text, reply_markup=item_detail_kb(item_id, cat_key))
    await callback.answer()


@router.callback_query(F.data == "back:categories")
async def back_to_categories(callback: CallbackQuery):
    await callback.message.edit_text("Выбери категорию:", reply_markup=categories_kb())
    await callback.answer()
