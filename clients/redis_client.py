import logging

from redis.asyncio import Redis, ConnectionPool

from config import env_vars, settings

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        self.client = None

    
    async def connect(self):
        logger.info("Connecting Redis client...")
        redis_connection_pool = ConnectionPool(
            host=env_vars.REDIS_HOST,
            port=env_vars.REDIS_PORT,
            db=env_vars.REDIS_DB,
            decode_responses=True,
            max_connections=settings.REDIS_MAX_CONNECTIONS
        )
        self.client = Redis(
            connection_pool=redis_connection_pool
        )
        logger.info("Redis client connected successfully.")


    async def disconnect(self):
        logger.info("Disconnecting Redis client...")
        if self.client:
            await self.client.close()
            self.client = None
        logger.info("Redis client disconnected successfully.")


redis_manager = RedisClient()