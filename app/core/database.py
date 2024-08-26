import pickle
from typing import AsyncGenerator
from typing import Optional, List

from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import settings


class DatabaseManager:
    def __init__(self, url: str, echo: bool, echo_pool: bool, pool_size: int, max_overflow: int) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow
        )
        self.session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session() as session:
            yield session

    async def dispose_engine(self) -> None:
        await self.engine.dispose()


database_manager = DatabaseManager(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)


class RedisManager:
    def __init__(self, redis_url: str) -> None:
        self.redis = aioredis.from_url(url=redis_url)

    async def close(self) -> None:
        await self.redis.close()

    async def get(self, key: str) -> Optional[List]:
        cached_data = await self.redis.get(key)
        if cached_data:
            return pickle.loads(cached_data)
        return None

    async def set(self, key: str, value: object, expire=3600) -> None:
        await self.redis.set(key, pickle.dumps(value), ex=expire)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)


redis_manager = RedisManager(redis_url=settings.caching.redis_url)
