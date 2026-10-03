from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

import domain
from db import models
from dto import Catalog


class CatalogRepository:
    def __init__(self, session: AsyncSession, registry):
        self._session = session
        self._registry = registry

    @staticmethod
    def _build_query(
        *,
        model,
        order_by,
        offset: int,
        limit: int,
    ):
        return (
            select(
                model,
                func.count(model.id)
                .over()
                .label("total"),
            )
            .order_by(order_by)
            .offset(offset)
            .limit(limit)
        )

    async def _execute(self, stmt) -> Catalog:
        result = await self._session.execute(stmt)
        rows = result.all()

        return Catalog(
            content=tuple(
                self._registry.to_domain(row[0])
                for row in rows
            ),
            total=rows[0].total if rows else 0,
        )


    async def get_services(
        self,
        *,
        category_id: int | None = None,
        offset: int = 0,
        limit: int = 5,
    ) -> Catalog[domain.Service]:
        stmt = self._build_query(
            model=models.Service,
            order_by=models.Service.position,
            offset=offset,
            limit=limit,
        )
        stmt = stmt.where(models.Service.category_id==category_id) if category_id is not None else stmt

        return await self._execute(stmt)


    async def get_categories(
        self,
        *,
        offset: int = 0,
        limit: int = 5,
    ) -> Catalog[domain.Category]:
        stmt = self._build_query(
            model=models.Category,
            order_by=models.Category.position,
            offset=offset,
            limit=limit,
        )

        return await self._execute(stmt)
