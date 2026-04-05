import random
import string
import asyncio
from telegram import Bot
from telegram.error import TelegramError

# Замените на ваш токен бота (получите у @BotFather)
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

def generate_username(length=8):
    """Генерирует случайный username заданной длины."""
    characters = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(characters) for _ in range(length))
    return username

async def is_username_available(username: str) -> bool:
    """
    Проверяет, свободен ли username в Telegram.
    Возвращает True, если свободен, False — если занят или недопустим.
    """
    bot = Bot(token=BOT_TOKEN)
    try:
        # Пытаемся установить username для бота. Если успешно — значит, свободен.
        result = await bot.set_my_username(f"@{username}")
        return result
    except TelegramError as e:
        error_message = str(e).lower()
        # Если ошибка связана с занятостью username
        if "username_occupied" in error_message or "username not available" in error_message:
            return False
        # Другие ошибки (недопустимый формат и т. д.) тоже считаем занятым
        else:
            print(f"Ошибка при проверке '{username}': {e}")
            return False

async def generate_free_username(max_attempts=100, username_length=8) -> str | None:
    """
    Генерирует свободный username.
    Пробует до max_attempts раз.
    Возвращает username или None, если не удалось найти свободный.
    """
    for attempt in range(1, max_attempts + 1):
        username = generate_username(username_length)
        print(f"Попытка {attempt}: проверяем '{username}'...")

        if await is_username_available(username):
            print(f"✓ Найден свободный username: {username}")
            return username
        # Небольшая задержка, чтобы не превысить лимиты Telegram API
        await asyncio.sleep(1)

    print("❌ Не удалось найти свободный username за заданное число попыток.")
    return None

# Основная функция для запуска
async def main():
    free_username = await generate_free_username(max_attempts=20, username_length=6)
    if free_username:
        print(f"\nИтоговый свободный username: @{free_username}")
    else:
        print("\nНе удалось сгенерировать свободный username.")

# Запуск
if __name__ == "__main__":
    asyncio.run(main())
