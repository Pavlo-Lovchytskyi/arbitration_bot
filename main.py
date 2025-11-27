import asyncio
import aiohttp

from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from listings.search import print_coin
from listings.monitoring import monitor_claim, active_claims


load_dotenv()

TOKEN = str(getenv("BOT_TOKEN"))

dp = Dispatcher()

@dp.message(Command("claim"))
async def claim_command(message: Message):
    args = message.text.split()
    if len(args) != 3:
        await message.answer("Использование: /claim <сеть: bnb|eth> <адрес>\nПример: /claim bnb 0x...")
        return

    network, address = args[1], args[2]
    await message.answer(f"Запущен мониторинг...")

    task = asyncio.create_task(monitor_claim(message, network, address))
    active_claims[message.from_user.id] = task

@dp.message(Command("stopclaim"))
async def stop_claim_command(message: Message):
    task = active_claims.get(message.from_user.id)
    if task and not task.done():
        task.cancel()
    else:
        await message.answer("У вас нет активного мониторинга /claim.")

@dp.message(Command("listings"))
async def run(message: Message) -> None:
    await message.answer(f"Hello {message.from_user.username}\n{print_coin()}")

@dp.message(Command("help"))
async def help (message: Message) -> None:
    await message.answer("/listings - листинги с сервиса icoanalytics.org.\n "
                         "/claim {сеть} {адрес} - запускает мониторинг метода клейм в выбраной сети и по контракту.\n " \
                         "/stopclaim - останавливает поиск.")

async def run_bot() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(run_bot())
