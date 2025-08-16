import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

inventory = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я склад-бот. Используй /add, /take, /list.")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Формат: /add товар количество")
        return
    item = context.args[0]
    qty = int(context.args[1])
    inventory[item] = inventory.get(item, 0) + qty
    await update.message.reply_text(f"✅ Добавлено: {item} ({inventory[item]})")

async def take(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Формат: /take товар количество")
        return
    item = context.args[0]
    qty = int(context.args[1])
    if item in inventory:
        inventory[item] = max(0, inventory[item] - qty)
        await update.message.reply_text(f"✂️ Забрано: {item} ({inventory[item]})")
    else:
        await update.message.reply_text("❌ Такого товара нет на складе")

async def list_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not inventory:
        await update.message.reply_text("Склад пуст")
        return
    text = "\n".join([f"{k}: {v}" for k,v in inventory.items()])
    await update.message.reply_text("📦 Остатки:\n" + text)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("take", take))
app.add_handler(CommandHandler("list", list_items))

if __name__ == "__main__":
    app.run_polling()
