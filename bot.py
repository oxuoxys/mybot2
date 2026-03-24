import logging
from telethon import TelegramClient, events, Button

# --- НАСТРОЙКИ ---
# Получите api_id и api_hash на https://my.telegram.org
API_ID = 1234567  # Замените на ваш
API_HASH = 'ваш_хэш' 
TOKEN = "8777938606:AAEYfh0pLyGdxp8nZMs2MM_bg5UdkzTgkL8"
ADMIN_ID = 850268482

# Инициализация клиента (как бота)
client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=TOKEN)

# --- КЛАВИАТУРЫ ---

def main_menu_kb():
    return [
        [Button.text("💎 Платные услуги"), Button.text("🎁 Бесплатные услуги")],
        [Button.text("💰 Поддержать автора")]
    ]

def free_services_inline_kb():
    return [
        [Button.inline("💿 ISO Образ Windows", b"free_windows")],
        [Button.inline("⚙️ Оптимизация Windows", b"free_opt")],
        [Button.inline("🔑 Активация Windows", b"free_act")]
    ]

# --- ХЕНДЛЕРЫ ---

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    sender = await event.get_sender()
    name = sender.first_name if sender.first_name else "Пользователь"
    await event.respond(
        f"Привет, {name}! 👋\nВыбери нужный пункт из меню ниже:",
        buttons=main_menu_kb()
    )

@client.on(events.NewMessage(pattern="💎 Платные услуги"))
async def paid_services(event):
    text = (
        "**💎 Наши платные услуги:**\n\n• Полная настройка под ключ\n• Удаленная помощь\n\n"
        "__Напиши сообщение здесь, чтобы связаться с мастером.__"
    )
    await event.respond(text, parse_mode="md")

@client.on(events.NewMessage(pattern="🎁 Бесплатные услуги"))
async def free_services(event):
    await event.respond("**🎁 Список бесплатных услуг:**", buttons=free_services_inline_kb(), parse_mode="md")

@client.on(events.NewMessage(pattern="💰 Поддержать автора"))
async def support_author(event):
    text = (
        "Спасибо что хочешь поддержать мой проект, поддержать можно переводом на карту:\n\n"
        "`2200 2061 0291 2966` (сбер)\n\n"
        "__(Нажми на номер выше, чтобы он скопировался)__"
    )
    await event.respond(text, parse_mode="md")

# --- ОБРАБОТКА НАЖАТИЙ (Inline) ---

@client.on(events.CallbackQuery(data=b"free_windows"))
async def handle_free_win(event):
    await event.respond(
        "К сожалению, выдача образов пока в разработке, но вы можете получить "
        "бесплатные ISO образы в боте @WinISO_bot"
    )
    await event.answer()

@client.on(events.CallbackQuery(data=b"free_opt"))
async def handle_opt(event):
    text = (
        "**⚙️ Инструкция по оптимизации ПК:**\n\n"
        "1. **Обязательно** создайте точку восстановления.\n"
        "2. Правой кнопкой на «Пуск» -> **PowerShell (Админ)**.\n"
        "3. Вставьте команду:\n\n"
        "`irm https://christitus.com | iex`\n\n"
        "4. В разделе **Tweaks** нажмите **Standard**, затем **Run Tweaks**."
    )
    await event.respond(text, parse_mode="md")
    await event.answer()

@client.on(events.CallbackQuery(data=b"free_act"))
async def handle_activation(event):
    text = (
        "**🔑 Инструкция по активации Windows:**\n\n"
        "1. Правой кнопкой на «Пуск» -> **PowerShell (Админ)**.\n"
        "2. Введите команду:\n\n"
        "`irm https://get.activated.win | iex`\n\n"
        "3. Нажмите клавишу **1** на клавиатуре."
    )
    await event.respond(text, parse_mode="md")
    await event.answer()

# --- ЛОГИКА ОБРАТНОЙ СВЯЗИ ---

@client.on(events.NewMessage())
async def feedback_logic(event):
    if event.is_private:
        # Игнорируем команды и кнопки меню
        if event.text in ["/start", "💎 Платные услуги", "🎁 Бесплатные услуги", "💰 Поддержать автора"]:
            return

        sender = await event.get_sender()
        
        # Если пишет НЕ админ — пересылаем админу
        if event.chat_id != ADMIN_ID:
            await event.reply("✅ Сообщение отправлено! Мастер ответит вам здесь.")
            info = f"📩 **От:** {sender.first_name}\nID: `{event.chat_id}`"
            await client.send_message(ADMIN_ID, info, parse_mode="md")
            await client.forward_messages(ADMIN_ID, event.message)
        
        # Если пишет админ В ОТВЕТ на сообщение
        elif event.chat_id == ADMIN_ID and event.is_reply:
            reply_msg = await event.get_reply_message()
            # Пробуем достать ID из пересланного сообщения
            if reply_msg.forward:
                target_id = reply_msg.forward.sender_id
                try:
                    await client.send_message(target_id, f"**Ответ мастера:**\n\n{event.text}")
                    await event.respond("✅ Ответ доставлен.")
                except Exception as e:
                    await event.respond(f"❌ Ошибка: {e}")

# Запуск
print("Бот запущен...")
client.run_until_disconnected()
