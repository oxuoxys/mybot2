import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import FSInputFile
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
    builder.row(types.InlineKeyboardButton(text="💿 ISO Образ Windows", callback_data="iso_menu"))
    builder.row(types.InlineKeyboardButton(text="📊 Microsoft Office", callback_data="office_menu"))
    builder.row(types.InlineKeyboardButton(text="⚙️ Оптимизация Windows", callback_data="free_opt"))
    builder.row(types.InlineKeyboardButton(text="🔑 Активация Windows", callback_data="free_act"))
    builder.row(types.InlineKeyboardButton(text="🛡 Windows Defender Remover", callback_data="free_defender"))
    builder.row(types.InlineKeyboardButton(text="💾 Rufus", callback_data="free_rufus"))
    builder.adjust(1)
    return builder.as_markup()

def iso_versions_kb():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Windows 10", callback_data="iso_win10"))
    builder.row(types.InlineKeyboardButton(text="Windows 11", url="https://t.me/oxuoxys_iso/5"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_free"))
    return builder.as_markup()

def win10_arch_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="x64 (64 бит)", url="https://t.me/oxuoxys_iso_3/4"),
        types.InlineKeyboardButton(text="x86 (32 бит)", url="https://t.me/oxuoxys_iso_2/5")
    )
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="iso_menu"))
    return builder.as_markup()

def office_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Office 2024", url="https://t.me/oxuoxys_office/3"))
    builder.row(types.InlineKeyboardButton(text="Office 2021", url="https://t.me/oxuoxys_office_2/3"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_free"))
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

# Навигация и меню
@dp.callback_query(F.data == "iso_menu")
async def handle_iso_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите версию Windows:", reply_markup=iso_versions_kb())
    await callback.answer()

@dp.callback_query(F.data == "iso_win10")
async def handle_win10_select(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите разрядность для Windows 10:", reply_markup=win10_arch_kb())
    await callback.answer()

@dp.callback_query(F.data == "office_menu")
async def handle_office_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите версию Microsoft Office:", reply_markup=office_menu_kb())
    await callback.answer()

@dp.callback_query(F.data == "back_to_free")
async def handle_back_free(callback: types.CallbackQuery):
    await callback.message.edit_text("<b>🎁 Список бесплатных услуг:</b>", reply_markup=free_services_inline_kb(), parse_mode="HTML")
    await callback.answer()

# Оптимизация
@dp.callback_query(F.data == "free_opt")
async def handle_opt(callback: types.CallbackQuery):
    text = (
        "<b>⚙️ Инструкция по оптимизации ПК:</b>\n\n"
        "Чтобы ускорить ваш компьютер, следуйте этим шагам:\n\n"
        "1. <b>Обязательно</b> создайте точку восстановления в Windows перед началом.\n"
        "2. Нажмите <b>правой кнопкой мыши</b> на кнопку «Пуск».\n"
        "3. Выберите <b>PowerShell (Админ)</b>.\n"
        "4. Скопируйте и вставьте команду:\n"
        "<code>irm https://christitus.com | iex</code>\n\n"
        "5. В открывшемся окне перейдите в раздел <b>Tweaks</b>.\n"
        "6. Нажмите на кнопку <b>Standard</b>.\n"
        "7. Нажмите <b>Run Tweaks</b> и дождитесь завершения процесса."
    )
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()

# Активация
@dp.callback_query(F.data == "free_act")
async def handle_activation(callback: types.CallbackQuery):
    text = (
        "<b>🔑 Инструкция по активации Windows:</b>\n\n"
        "Чтобы активировать Windows навсегда, выполните действия:\n\n"
        "1. Нажмите <b>правой кнопкой мыши</b> на кнопку «Пуск».\n"
        "2. Выберите <b>PowerShell (Админ)</b>.\n"
        "3. Вставьте команду:\n"
        "<code>irm https://get.activated.win | iex</code>\n\n"
        "4. Нажмите Enter и дождитесь открытия окна.\n"
        "5. В открывшемся окне нажмите клавишу <b>1</b> на клавиатуре."
    )
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()

# Файлы
@dp.callback_query(F.data == "free_defender")
async def handle_defender(callback: types.CallbackQuery):
    file_path = "Windows_Defender_Remover.exe"
    if os.path.exists(file_path):
        await callback.message.answer_document(
            FSInputFile(file_path), 
            caption="Запустить, нажать <b>A</b> и Enter.", 
            parse_mode="HTML"
        )
    else:
        await callback.message.answer("❌ Файл Windows_Defender_Remover.exe не найден.")
    await callback.answer()

@dp.callback_query(F.data == "free_rufus")
async def handle_rufus(callback: types.CallbackQuery):
    file_path = "Rufus.exe"
    if os.path.exists(file_path):
        await callback.message.answer_document(
            FSInputFile(file_path), 
            caption="Программа для записи ISO на флешку.", 
            parse_mode="HTML"
        )
    else:
        await callback.message.answer("❌ Файл Rufus.exe не найден.")
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
        target_id = message.reply_to_message.forward_from.id if message.reply_to_message.forward_from else None
        if target_id:
            await bot.send_message(target_id, f"<b>Ответ мастера:</b>\n\n{message.text}", parse_mode="HTML")
            await message.answer("✅ Ответ доставлен.")
    except Exception:
        await message.answer("❌ Ошибка отправки.")

# --- ЗАПУСК ---
async def main():
    logging.basicConfig(level=logging.INFO)
    asyncio.create_task(start_web_server())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
