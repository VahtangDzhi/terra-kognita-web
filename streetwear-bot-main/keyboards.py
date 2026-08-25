"""
Все клавиатуры бота собраны здесь, отдельно от логики хендлеров.
Так проще найти и поправить любую кнопку без поиска по всему проекту.
"""

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import CATALOG, FAQ


def main_menu_kb() -> ReplyKeyboardMarkup:
    """Главное меню — постоянная клавиатура внизу экрана."""
    builder = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍 Каталог"), KeyboardButton(text="❓ FAQ")],
            [KeyboardButton(text="✉️ Связаться с менеджером")],
        ],
        resize_keyboard=True,
    )
    return builder


def categories_kb() -> InlineKeyboardMarkup:
    """Список категорий товаров."""
    builder = InlineKeyboardBuilder()
    for cat_key, cat in CATALOG.items():
        builder.button(text=cat["title"], callback_data=f"cat:{cat_key}")
    builder.adjust(2)
    return builder.as_markup()


def items_kb(cat_key: str) -> InlineKeyboardMarkup:
    """Список товаров внутри категории + кнопка назад."""
    builder = InlineKeyboardBuilder()
    for item in CATALOG[cat_key]["items"]:
        builder.button(
            text=f"{item['name']} — {item['price']}₽",
            callback_data=f"item:{item['id']}",
        )
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="⬅️ Назад к категориям", callback_data="back:categories"))
    return builder.as_markup()


def item_detail_kb(item_id: str, cat_key: str) -> InlineKeyboardMarkup:
    """Карточка товара: кнопка заказать + назад."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🛒 Заказать", callback_data=f"order:{item_id}")
    builder.button(text="⬅️ Назад", callback_data=f"cat:{cat_key}")
    builder.adjust(1)
    return builder.as_markup()


def sizes_kb(item_id: str) -> InlineKeyboardMarkup:
    """Выбор размера на старте заказа."""
    from data import find_item

    _, item = find_item(item_id)
    builder = InlineKeyboardBuilder()
    for size in item["sizes"]:
        builder.button(text=size, callback_data=f"size:{size}")
    builder.adjust(len(item["sizes"]))
    return builder.as_markup()


def confirm_order_kb() -> InlineKeyboardMarkup:
    """Подтверждение заказа в самом конце."""
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Подтвердить заказ", callback_data="confirm_order")
    builder.button(text="❌ Отменить", callback_data="cancel_order")
    builder.adjust(1)
    return builder.as_markup()


def faq_kb() -> InlineKeyboardMarkup:
    """Список вопросов FAQ."""
    builder = InlineKeyboardBuilder()
    for q in FAQ:
        builder.button(text=q["q"], callback_data=f"faq:{q['id']}")
    builder.adjust(1)
    return builder.as_markup()


def back_to_faq_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад к вопросам", callback_data="back:faq")
    return builder.as_markup()
