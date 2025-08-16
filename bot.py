import os
import re
from collections import defaultdict
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import html

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Положите сюда токен

bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# Простое «хранилище» в памяти (имя -> количество)
# Для продакшена замените на БД (SQLite/Postgres и т.п.)
stock = defaultdict(int)

def parse_item_with_qty(text: str, cmd: str) -> tuple[str, int] | None:
    """
    Разбирает строку вида:
      /add Spirit 48
      /take Coca Cola 5
    Возвращает (name, qty) или None.
    """
    # Берём всё, что после команды, и делим: последняя "группа" — число
    m = re.match(rf"^/{cmd}\s+(.+)\s+(-?\d+)\s*$", text, flags=re.IGNORECASE)
    if not m:
        return None
    name = m.group(1).strip()
    qty = int(m.group(2))
    return name, qty

def fmt_stock() -> str:
    if not stock:
        return "Склад пуст."
    lines = ["<b>Текущие остатки:</b>"]
    for name, qty in sorted(stock.items(), key=lambda x: x[0].lower()):
        # экранируем спецсимволы для HTML-разметки
        lines.append(f"• {html.quote(name)} — <b>{qty}</b>")
    return "\n".join(lines)

@dp.message(CommandStart())
async def cmd_start(m: Message):
    await m.reply("Бот на вебхуках ✅\n\n"
                  "Команды:\n"
                  "/add <название> <кол-во>\n"
                  "/take <название> <кол-во>\n"
                  "/list — показать склад\n"
                  "/remove <название> — удалить позицию\n"
                  "/help — помощь")

@dp.message(Command("help"))
async def cmd_help(m: Message):
    await m.reply(
        "Примеры:\n"
        "/add Spirit 48\n"
        "/take Spirit 5\n"
        "/list\n"
        "/remove Spirit"
    )

@dp.message(F.text.regexp(r"^/add\b", flags=re.IGNORECASE))
async def cmd_add(m: Message):
    parsed = parse_item_with_qty(m.text, "add")
    if not parsed:
        return await m.reply("Формат: <code>/add Название 10</code>")
    name, qty = parsed
    if qty <= 0:
        return await m.reply("Количество должно быть положительным.")
    stock[name] += qty
    await
