from .start import router as start_router
from .catalog import router as catalog_router
from .faq import router as faq_router
from .order import router as order_router

# Список всех роутеров — main.py подключает их одним циклом
all_routers = [start_router, catalog_router, faq_router, order_router]
