from html import escape

from domain import Service

SERVICES = (
    "<b>Каталог услуг</b>\n\n"
    "Выберите интересующую услугу."
)

CATEGORIES = (
    "<b>Категории услуг</b>\n\n"
    "Выберите категорию, чтобы посмотреть доступные услуги."
)

EMPTY_SERVICES = "Услуги пока отсутствуют."

EMPTY_CATEGORIES = "Категории пока отсутствуют."


def category_services(category: str) -> str:
    return (
        f"<b>{escape(category)}</b>\n\n"
        "Доступные услуги в этой категории:"
    )

def service_card(service: Service) -> str:
    return (
        f"<b>{escape(service.title)}</b>\n\n"
        f"{escape(service.description)}\n\n"
        f"💰 Цена от: {service.price_from}"
    )