"""
Состояния для пошагового диалога оформления заказа (FSM — Finite State Machine).

Идея простая: пока пользователь "находится" в одном из этих состояний,
бот ждёт от него конкретный тип ответа (например, телефон), и обрабатывает
именно его, а не запускает остальные хендлеры.
"""

from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    waiting_size = State()
    waiting_name = State()
    waiting_phone = State()
    waiting_city = State()
    confirm = State()
