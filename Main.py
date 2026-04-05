import random
import string
import asyncio
from telethon import TelegramClient

# Данные API (получите на my.telegram.org)
API_ID = 'your_api_id'
API_HASH = 'your_api_hash'

# Номер телефона привязанного аккаунта
PHONE_NUMBER = '+71234567890'

def generate_username(length=8):
    """Генерирует случайный username заданной длины."""
    characters = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(characters) for _ in range(length))
    return username

async def is_username_available(username: str) -> bool:
    """Проверяет, свободен ли username в Telegram."""
    async with TelegramClient(PHONE_NUMBER, API_ID, API_HASH) as client:
        try:
            result = await client.is_username_available(username)
            return result
        except Exception as e:
            print(f"Ошибка при проверке '{username}': {e}")
            return False

async def generate_free_username(max_attempts=100, username_length=8) -> str | None:
    """Генерирует свободный username."""
    for attempt in range(1, max_attempts + 1):
        username = generate_username(username_length)
        print(f"Попытка {attempt}: проверяем '{username}'...")

        if await is_username_available(username):
            print(f"✓ Найден свободный username: {username}")
            return username
        await asyncio.sleep(1)

    print("❌ Не удалось найти свободный username за заданное число попыток.")
    return None

async def main():
    free_username = await generate_free_username(max_attempts=20, username_length=6)
    if free_username:
        print(f"\nИтоговый свободный username: @{free_username}")
    else:
        print("\nНе удалось сгенерировать свободный username.")

if __name__ == "__main__":
    asyncio.run(main())
