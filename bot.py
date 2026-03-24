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

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER (Keep-alive) ---
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
    await message.answer(f"Привет, {message.from_user.first_name}! 👋\nВыбери нужный пункт из меню ниже:", reply_markup=main_menu_kb())

@dp.message(F.text == "💎 Платные услуги")
async def paid_services(message: types.Message):
    await message.answer(
        "<b>💎 Наши платные услуги:</b>\n\n"
        "• Полная настройка системы под ключ\n"
        "• Удаленная помощь через AnyDesk\n\n"
        "<i>Напиши сюда свой вопрос, чтобы связаться с мастером.</i>", 
        parse_mode="HTML"
    )

@dp.message(F.text == "🎁 Бесплатные услуги")
async def free_services(message: types.Message):
    await message.answer("<b>🎁 Список бесплатных услуг:</b>", reply_markup=free_services_inline_kb(), parse_mode="HTML")

@dp.callback_query(F.data == "free_windows")
async def handle_free_win(callback: types.CallbackQuery):
    await callback.message.answer("К сожалению, выдача образов пока в разработке, но вы можете получить бесплатные ISO образы в боте @WinISO_bot")
    await callback.answer()

@dp.callback_query(F.data == "free_opt")
async def handle_opt(callback: types.CallbackQuery):
    text = (
        "<b>⚙️ Инструкция по оптимизации ПК:</b>\n\n"
        "Чтобы ускорить ваш компьютер, следуйте этим шагам:\n\n"
        "1. <b>Обязательно</b> создайте точку восстановления в Windows перед началом.\n"
        "2. Нажмите <b>правой кнопкой мыши</b> на кнопку «Пуск».\n"
        "3. Выберите <b>PowerShell (Админ)</b> или <b>Terminal (Admin)</b>.\n"
        "4. Скопируйте и вставьте следующую команду:\n\n"
        "<code>irm https://christitus.com | iex</code>\n\n"
        "5. В открывшемся окне перейдите в раздел <b>Tweaks</b>.\n"
        "6. Нажмите на кнопку <b>Standard</b>.\n"
        "7. Нажмите <b>Run Tweaks</b> и дождитесь завершения процесса.\n\n"
        "<i>(Команда выше копируется автоматически при нажатии)</i>"
    )
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "free_act")
async def handle_activation(callback: types.CallbackQuery):
    text = (
        "<b>🔑 Инструкция по активации Windows:</b>\n\n"
        "Чтобы активировать Windows навсегда, выполните следующие действия:\n\n"
        "1. Нажмите <b>правой кнопкой мыши</b> на кнопку «Пуск».\n"
        "2. Выберите <b>Terminal (Admin)</b> или <b>PowerShell (Админ)</b>.\n"
        "3. Скопируйте и вставьте команду ниже:\n\n"
        "<code>irm https://get.activated.win | iex</code>\n\n"
        "4. Нажмите Enter и дождитесь открытия окна.\n"
        "5. В открывшемся окне нажмите клавишу <b>1</b> на клавиатуре.\n\n"
        "<i>(Нажмите на команду выше, чтобы она скопировалась автоматически)</i>"
    )
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()

@dp.message(F.text == "💰 Поддержать автора")
async def support_author(message: types.Message):
    await message.answer(
        "Спасибо что хочешь поддержать мой проект, поддержать можно переводом на карту:\n\n"
        "<code>2200 2061 0291 2966</code> (сбер)\n\n"
        "<i>(Нажми на номер выше, чтобы он скопировался)</i>", 
        parse_mode="HTML"
    )

# --- ОБРАТНАЯ СВЯЗЬ ---
@dp.message(F.chat.id != ADMIN_ID)
async def forward_to_admin(message: types.Message):
    if message.text in ["💎 Платные услуги", "🎁 Бесплатные услуги", "💰 Поддержать автора"]:
        return
    await message.reply("✅ Сообщение отправлено! Мастер ответит вам здесь.")
    await bot.send_message(ADMIN_ID, f"📩 <b>От:</b> {message.from_user.full_name}\nID: <code>{message.from_user.id}</code>", parse_mode="HTML")
    await message.send_copy(chat_id=ADMIN_ID)

@dp.message(F.chat.id == ADMIN_ID, F.reply_to_message)
async def reply_to_user(message: types.Message):
    try:
        # Пытаемся достать ID из уведомления или пересылки
        target_id = message.reply_to_message.forward_from.id if message.reply_to_message.forward_from else None
        
        if target_id:
            await bot.send_message(target_id, f"<b>Ответ мастера:</b>\n\n{message.text}", parse_mode="HTML")
            await message.answer("✅ Ответ доставлен.")
        else:
            await message.answer("❌ Не удалось определить ID пользователя (скрыт приватностью).")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

# --- ЗАПУСК ---
async def main():
    logging.basicConfig(level=logging.INFO)
    asyncio.create_task(start_web_server())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
