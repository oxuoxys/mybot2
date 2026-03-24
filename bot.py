import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiohttp import web

# --- НАСТРОЙКИ ---
TOKEN = os.getenv("BOT_TOKEN", "8777938606:AAEYfh0pLyGdxp8nZMs2MM_bg5UdkzTgkL8")
ADMIN_ID = 850268482

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER ---
async def handle(request):
    return web.Response(text="Bot is running 24/7!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# --- КЛАВИАТУРЫ ---
def main_menu_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="💎 Платные услуги")
    kb.button(text="🎁 Бесплатные услуги")
    kb.button(text="💰 Поддержать автора")
    kb.adjust(2, 1)
    return kb.as_markup(resize_keyboard=True)

def free_services_inline_kb():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="💿 ISO Образ Windows", callback_data="free_windows"))
    builder.row(types.InlineKeyboardButton(text="⚙️ Оптимизация Windows", callback_data="free_opt"))
    builder.row(types.InlineKeyboardButton(text="🔑 Активация Windows", callback_data="free_act"))
    return builder.as_markup()

# --- ХЕНДЛЕРЫ ---
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}! 👋\nВыбери пункт из меню:", reply_markup=main_menu_kb())

@dp.message(F.text == "💎 Платные услуги")
async def paid_services(message: types.Message):
    await message.answer("<b>💎 Наши платные услуги:</b>\n\n• Полная настройка под ключ\n• Удаленная помощь", parse_mode="HTML")

@dp.message(F.text == "🎁 Бесплатные услуги")
async def free_services(message: types.Message):
    await message.answer("<b>🎁 Список бесплатных услуг:</b>", reply_markup=free_services_inline_kb(), parse_mode="HTML")

@dp.callback_query(F.data == "free_windows")
async def handle_free_win(callback: types.CallbackQuery):
    await callback.message.answer("Выдача образов в разработке, загляните в @WinISO_bot")
    await callback.answer()

@dp.callback_query(F.data == "free_opt")
async def handle_opt(callback: types.CallbackQuery):
    await callback.message.answer("<b>⚙️ Оптимизация:</b>\nИспользуйте команду: <code>irm https://christitus.com | iex</code>", parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "free_act")
async def handle_activation(callback: types.CallbackQuery):
    await callback.message.answer("<b>🔑 Активация:</b>\nКоманда: <code>irm https://get.activated.win | iex</code>", parse_mode="HTML")
    await callback.answer()

@dp.message(F.text == "💰 Поддержать автора")
async def support_author(message: types.Message):
    await message.answer("Карта: <code>2200 2061 0291 2966</code>", parse_mode="HTML")

# --- ОБРАТНАЯ СВЯЗЬ ---
@dp.message(F.chat.id != ADMIN_ID)
async def forward_to_admin(message: types.Message):
    if message.text in ["💎 Платные услуги", "🎁 Бесплатные услуги", "💰 Поддержать автора"]:
        return
    await message.reply("✅ Сообщение отправлено!")
    await bot.send_message(ADMIN_ID, f"📩 <b>От:</b> {message.from_user.full_name}\nID: <code>{message.from_user.id}</code>", parse_mode="HTML")
    await message.send_copy(chat_id=ADMIN_ID)

@dp.message(F.chat.id == ADMIN_ID, F.reply_to_message)
async def reply_to_user(message: types.Message):
    try:
        target_id = message.reply_to_message.forward_from.id if message.reply_to_message.forward_from else None
        if target_id:
            await bot.send_message(target_id, f"<b>Ответ мастера:</b>\n\n{message.text}", parse_mode="HTML")
            await message.answer("✅ Ответ доставлен.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

# --- ЗАПУСК ---
async def main():
    logging.basicConfig(level=logging.INFO)
    asyncio.create_task(start_web_server())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
