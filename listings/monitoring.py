import asyncio
import aiohttp

from aiogram.types import Message
from bs4 import BeautifulSoup as bs


active_claims = {}

async def check_claim(network: str, address: str):
    if network.lower() in ("bsc", "bnb"):
        base_url = "https://bscscan.com"
    elif network.lower() in ("eth", "ethereum"):
        base_url = "https://etherscan.io"
    else:
        return "unknown_network"

    addr_url = f"{base_url}/address/{address}"

    async with aiohttp.ClientSession() as session:
        async with session.get(addr_url) as resp:
            addr_html = await resp.text()

    soup_addr = bs(addr_html, "lxml")

    invalid_block = soup_addr.find("span", class_="me-3 fs-base")

    if invalid_block and "invalid address" in invalid_block.text.lower():
        return "invalid_address"

    txs_url = f"{base_url}/txs?a={address}"

    async with aiohttp.ClientSession() as session:
        async with session.get(txs_url) as resp:
            tx_html = await resp.text()

    soup_tx = bs(tx_html, "lxml")
    rows = soup_tx.select("table tbody tr")

    if not rows:
        return False

    for r in rows:
        if "claim" in r.text.lower():
            return True

    return False

async def monitor_claim(message: Message, network: str, address: str):
    try:
        while True:
            result = await check_claim(network, address)

            if result == "unknown_network":
                await message.answer("⚠️ Неизвестная сеть. Используй BSC или ETH.")
                break

            if result == "invalid_address":
                await message.answer(f"❌ Адрес {address} является НЕКОРРЕКТНЫМ!")
                break

            if result == "contract_not_found":
                await message.answer(f"❌ Контракт {address} не найден в сети {network.upper()}!")
                break

            if result is True:
                await message.answer(f"✅ Claim найден! Контракт {address}, сеть {network.upper()}.")
                break

            await asyncio.sleep(5)

    except asyncio.CancelledError:
        await message.answer("Мониторинг /claim остановлен.")
    finally:
        active_claims.pop(message.from_user.id, None)