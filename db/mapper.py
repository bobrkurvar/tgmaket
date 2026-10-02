from db import models
import domain


def map_category_to_orm(
    obj: domain.Category,
) -> models.Category:
    return models.Category(
        id=obj.id,
        name=obj.name,
        position=obj.position,
        is_active=obj.is_active,
    )


def map_category_to_domain(
    obj: models.Category,
) -> domain.Category:
    return domain.Category(
        id=obj.id,
        name=obj.name,
        position=obj.position,
        is_active=obj.is_active,
    )


def map_service_to_orm(
    obj: domain.Service,
) -> models.Service:
    return models.Service(
        id=obj.id,
        category_id=obj.category_id,
        title=obj.title,
        short_description=obj.short_description,
        description=obj.description,
        price_from=obj.price_from,
        image=obj.image,
        position=obj.position,
        is_active=obj.is_active,
    )


def map_service_to_domain(
    obj: models.Service,
) -> domain.Service:
    return domain.Service(
        id=obj.id,
        category_id=obj.category_id,
        title=obj.title,
        short_description=obj.short_description,
        description=obj.description,
        price_from=obj.price_from,
        image=obj.image,
        position=obj.position,
        is_active=obj.is_active,
    )


class MapperRegistry:
    def __init__(self):
        self._models = {}
        self._to_orm_funcs = {}
        self._to_dto_funcs = {}

    def register(
        self,
        dto_cls,
        orm_model,
        to_orm,
        to_dto,
    ):
        self._models[dto_cls] = orm_model
        self._to_orm_funcs[dto_cls] = to_orm
        self._to_dto_funcs[orm_model] = to_dto

    def get_model(self, dto_cls):
        return self._models[dto_cls]

    def to_orm(self, dto_obj):
        dto_cls = type(dto_obj)
        func = self._to_orm_funcs.get(dto_cls)

        if not func:
            raise RuntimeError(
                f"Маппер в ORM не найден для {dto_cls}"
            )

        return func(dto_obj)

    def to_dto(self, orm_obj):
        orm_cls = type(orm_obj)
        func = self._to_dto_funcs.get(orm_cls)

        if not func:
            raise RuntimeError(
                f"Маппер в Домен не найден для {orm_cls}"
            )

        return func(orm_obj)


registry = MapperRegistry()

registry.register(
    dto_cls=domain.Category,
    orm_model=models.Category,
    to_orm=map_category_to_orm,
    to_dto=map_category_to_domain,
)

registry.register(
    dto_cls=domain.Service,
    orm_model=models.Service,
    to_orm=map_service_to_orm,
    to_dto=map_service_to_domain,
)