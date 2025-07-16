SESSION = '''import asyncio
import functools
import logging
from contextlib import asynccontextmanager, contextmanager
from typing import Any, AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.exc import DisconnectionError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings

logger = logging.getLogger(__name__)


# connection pool configuration
CONNECTION_POOL_CONFIG = {"echo": settings.DEV_LOGS}

if settings.DB_PORT == "5432":
    # session mode
    CONNECTION_POOL_CONFIG.update(
        {
            "pool_size": 10,
            "max_overflow": 20,
            "pool_timeout": 30,
            "pool_recycle": 3600,
            "pool_pre_ping": True,
        }
    )
elif settings.DB_PORT == "6543":
    # transaction mode
    CONNECTION_POOL_CONFIG["poolclass"] = NullPool
else:
    raise ValueError(f"Invalid database port: {settings.DB_PORT}")

# synchronous session
engine = create_engine(
    settings.supabase_connection_string,
    **CONNECTION_POOL_CONFIG,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# asynchronous session
async_engine = create_async_engine(
    settings.async_supabase_connection_string,
    **CONNECTION_POOL_CONFIG,
)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


def retry_db_operation(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator to retry database operations on connection failures.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except (OperationalError, DisconnectionError) as e:
                    last_exception = e
                    error_msg = str(e).lower()

                    # check if it's a connection-related error
                    if any(
                        phrase in error_msg
                        for phrase in [
                            "server closed the connection",
                            "connection closed",
                            "connection was closed",
                            "connection terminated",
                            "connection lost",
                            "connection reset",
                        ]
                    ):
                        if attempt < max_retries:
                            logger.warning(
                                f"Database connection failed (attempt {attempt + 1}/{max_retries + 1}): {e}"
                            )
                            await asyncio.sleep(
                                delay * (attempt + 1)
                            )  # exponential backoff
                            continue

                    # for non-connection errors or max retries reached
                    raise
                except Exception:
                    # for non-connection exceptions, don't retry
                    raise

            # if we get here, all retries failed
            raise last_exception

        return wrapper

    return decorator


@contextmanager
def get_session() -> Generator[Any, Any, Any]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as adb:
        try:
            yield adb
        finally:
            await adb.close()


async def get_async_session_dep() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for async database session.

    Usage:
        @router.get("/endpoint")
        async def my_endpoint(session: AsyncSession = Depends(get_async_session_dep)):
            # Use session here
            pass
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


class BaseSession:
    def __init__(self):
        self.session = None
        self._session = None

    def __enter__(self):
        self._session = get_session()
        self.session = self._session.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            # log or handle the exception here
            pass
        else:
            self.session.commit()
        self.session.close()
        return self._session_cm.__exit__(exc_type, exc_val, exc_tb)
'''
