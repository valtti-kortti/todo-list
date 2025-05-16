from database.crud import setUser
import asyncio

async def main():
    await setUser(name="Egor", surname="Smirnov")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass