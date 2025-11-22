import asyncio
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from listings.search import print_coin

load_dotenv()

TOKEN = str(getenv("BOT_TOKEN"))

dp = Dispatcher()

@dp.message(Command("listings"))
async def run(message: Message) -> None:
    await message.answer(f"Hello {message.from_user.username}\n{print_coin()}")

@dp.message(Command("help"))
async def help (message: Message) -> None:
    await message.answer("/listings - listings on coin market cup service.\n ")

async def run_bot() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(run_bot())
