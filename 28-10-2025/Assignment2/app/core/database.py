# app/core/database.py

from app.prisma import Prisma
import logging

# Initialize Prisma client
db = Prisma()
logger = logging.getLogger("prisma_client")

# Connect to database
async def connect_db():
    try:
        await db.connect()
        logger.info(" Database connected successfully")
    except Exception as e:
        logger.error(f" Database connection failed: {e}")
        raise e

# Disconnect from database
async def disconnect_db():
    try:
        await db.disconnect()
        logger.info(" Database disconnected successfully")
    except Exception as e:
        logger.error(f"Database disconnection failed: {e}")
        raise e
