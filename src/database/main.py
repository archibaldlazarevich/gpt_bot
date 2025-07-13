import asyncio
from src.database.create_db import create_db

if __name__ == "__main__":
    try:
        asyncio.run(create_db())
    except KeyboardInterrupt:
        print("Scheduler interrupted by user")
