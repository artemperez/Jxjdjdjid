import logging
import random
import asyncio
import json
import aiohttp
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, 
    ReplyKeyboardMarkup, KeyboardButton,
    CallbackQuery
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import aiosqlite

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ваши данные
BOT_TOKEN = "8400770070:AAFahEEaffeqcI0kcMwq5QVlv0Aur1GdbA8"
OWNER_ID = 8050595279
OWNER_USERNAME = "@aurieza"
ADMIN_IDS = [OWNER_ID]

# Обязательные каналы для подписки
REQUIRED_CHANNELS = [
    {"username": "@Manuals_and_softs", "title": "Manuals and softs🔫", "link": "https://t.me/+uzhF2YtokTo2ZjBi"},
    {"username": "@Chat_zaisa", "title": "Чат зайса)", "link": "https://t.me/+JjhrjbcMMso2MGQy"}
]

# Все приватные каналы
ALL_PRIVATE_CHANNELS = [
    ("💎 Приват #1", "https://t.me/+ZuUNjg1bJ3xiOTIy"),
    ("🔥 Приват #2", "https://t.me/+ud0gESAJTRpiNGY6"),
    ("🌟 Приват #3", "https://t.me/+ImsOnVdV-wkzMzgy"),
    ("🚀 Приват #4", "https://t.me/+GoHxJYZjVHM2OTU8"),
    ("💫 Приват #5", "https://t.me/+OwCjJcf8MLMzMDY0"),
    ("🎯 Приват #6", "https://t.me/+7R5UlNBtS_ozMjI0"),
    ("⚡ Приват #7", "https://t.me/+EXlBIikoHqY5NjM0"),
    ("🎁 Приват #8", "https://t.me/+tB3ELsrzjXYxNTA8"),
    ("💝 Приват #9", "https://t.me/+XS93nu2kjkgwYzEy"),
    ("🎪 Приват #10", "https://t.me/+jtrr7X3DGJAyMzUy"),
    ("✨ Приват #11", "https://t.me/+CLvBRlmQyKRmZWNi"),
    ("🎭 Приват #12", "https://t.me/+vTldRbXSDx8yNzY6"),
    ("💼 Приват #13", "https://t.me/+qSvuUw3Xi0plMzVk"),
    ("🏆 Приват #14", "https://t.me/+3hsRBgNQeSA1Zjc0"),
    ("🎨 Приват #15", "https://t.me/+fun3xCBTTCphNDY6"),
    ("⚜️ Приват #16", "https://t.me/+_-ZMOq11be9lNWNi"),
    ("🔮 Приват #17", "https://t.me/+h_4WC3Kovq1iZjM0"),
    ("💸 Приват #18", "https://t.me/+5tPlzYo9dINjMGQ6"),
    ("🛡️ Приват #19", "https://t.me/+l6yx3GDPfZs3MTcy"),
    ("🎖️ Приват #20", "https://t.me/+JfWKSCrUdEQ4YmRi"),
    ("🎬 Приват #21", "https://t.me/+sGbKNtgrKzMzZWI0"),
    ("🎧 Приват #22", "https://t.me/+y0rpo4bAM6JmODAy"),
    ("🎸 Приват #23", "https://t.me/+GJS2mdhj5_JmYTBi"),
    ("📱 Приват #24", "https://t.me/+kpRNywup-tIyYzUy"),
    ("💻 Приват #25", "https://t.me/+Cim4j0KPWU0zZWJi"),
    ("🖥️ Приват #26", "https://t.me/+fsFDo_r5bBk0Yjk0"),
    ("📡 Приват #27", "https://t.me/+JMHlFI45ppw1ZDky"),
    ("🛰️ Приват #28", "https://t.me/+y4MMo2_f4DFmODNi"),
    ("🔭 Приват #29", "https://t.me/+Su7A6bDH_L8xYTUy"),
    ("🧬 Приват #30", "https://t.me/+uvzDdXuTeCU5NDRi"),
    ("🔬 Приват #31", "https://t.me/+2JJdqT5zSa0zMGM0"),
    ("🧪 Приват #32", "https://t.me/+C1S2zINTJ3ozYjc0"),
    ("⚗️ Приват #33", "https://t.me/+_JLaUwx6NiMzOGRi"),
    ("📊 Приват #34", "https://t.me/+t6dpNkkV2G4yZDli"),
    ("📈 Приват #35", "https://t.me/+EEwhazNzq5wzMjIy"),
    ("📉 Приват #36", "https://t.me/+DfyaUSyV4VU2NTZi"),
    ("💰 Приват #37", "https://t.me/+0uN0IYrraJswNmFk"),
    ("💎 Приват #38", "https://t.me/+xqJEiHkw-6FiNmJi"),
    ("🏦 Приват #39", "https://t.me/+Oolh-X6pIhhlYTMy"),
    ("💳 Приват #40", "https://t.me/+cLkkkmIwXYk4Yzcy"),
    ("🏠 Приват #41", "https://t.me/+HKiEUZGsqgNjZWQ8"),
    ("🏢 Приват #42", "https://t.me/+3QbqycNNYFI0ZjU6"),
    ("🏨 Приват #43", "https://t.me/+bt6iivf0tTtmNTE6"),
    ("🏩 Приват #44", "https://t.me/+JaQQu47vhDI2NmQy"),
    ("🏪 Приват #45", "https://t.me/+la195L2Vi6kwNGY6"),
    ("💰 Money приват", "https://t.me/money_privat"),
    ("🔐 Приват #47", "https://t.me/+2uZS1rkKYf0xYTQy"),
    ("🔒 Приват #48", "https://t.me/+MWPACm-3LfcyNDhi"),
    ("🔑 Приват #49", "https://t.me/+AX3nc3ccbsYzNDcy"),
    ("🗝️ Приват #50", "https://t.me/+pfwrCNbzufs4MmYy"),
]

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Инициализация базы данных
DB_NAME = "bot_database.db"

# Состояния FSM
class UserState(StatesGroup):
    waiting_captcha = State()
    waiting_subscription = State()
    reading_rules = State()
    ai_waiting_question = State()

class AdminState(StatesGroup):
    waiting_channel_username = State()
    waiting_channel_link = State()
    waiting_private_name = State()
    waiting_private_link = State()
    waiting_admin_id = State()
    waiting_broadcast = State()
    waiting_user_id = State()

# Класс для управления базой данных
class Database:
    def __init__(self):
        self.db_name = DB_NAME
        
    async def init_db(self):
        """Инициализация базы данных"""
        async with aiosqlite.connect(self.db_name) as db:
            # Таблица пользователей
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT,
                    captcha_passed BOOLEAN DEFAULT 0,
                    subscribed BOOLEAN DEFAULT 0,
                    rules_accepted BOOLEAN DEFAULT 0,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ai_requests INTEGER DEFAULT 0,
                    is_banned BOOLEAN DEFAULT 0
                )
            ''')
            
            # Таблица каналов для подписки
            await db.execute('''
                CREATE TABLE IF NOT EXISTS admin_channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_username TEXT UNIQUE,
                    channel_title TEXT,
                    channel_link TEXT,
                    added_by INTEGER,
                    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица приватных каналов
            await db.execute('''
                CREATE TABLE IF NOT EXISTS private_channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    link TEXT UNIQUE,
                    added_by INTEGER,
                    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица администраторов
            await db.execute('''
                CREATE TABLE IF NOT EXISTS admins (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    added_by INTEGER,
                    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица статистики
            await db.execute('''
                CREATE TABLE IF NOT EXISTS stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric TEXT,
                    value INTEGER,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            await db.commit()
            
            # Добавляем владельца как админа
            await self.add_admin(OWNER_ID, OWNER_USERNAME.split('@')[-1] if '@' in OWNER_USERNAME else OWNER_USERNAME, OWNER_ID)
            
            # Добавляем обязательные каналы
            for channel in REQUIRED_CHANNELS:
                try:
                    await self.add_admin_channel(
                        channel["username"], 
                        channel["title"], 
                        channel["link"], 
                        OWNER_ID
                    )
                except:
                    pass
            
            # Добавляем все приватные каналы
            for name, link in ALL_PRIVATE_CHANNELS:
                try:
                    await self.add_private_channel(name, link, OWNER_ID)
                except:
                    pass
    
    async def add_user(self, user_id: int, username: str, full_name: str):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                """INSERT OR IGNORE INTO users 
                (user_id, username, full_name) 
                VALUES (?, ?, ?)""",
                (user_id, username, full_name)
            )
            await db.commit()
    
    async def update_user_captcha(self, user_id: int, passed: bool = True):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "UPDATE users SET captcha_passed = ? WHERE user_id = ?",
                (passed, user_id)
            )
            await db.commit()
    
    async def update_user_subscription(self, user_id: int, subscribed: bool = True):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "UPDATE users SET subscribed = ? WHERE user_id = ?",
                (subscribed, user_id)
            )
            await db.commit()
    
    async def update_user_rules(self, user_id: int, accepted: bool = True):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "UPDATE users SET rules_accepted = ? WHERE user_id = ?",
                (accepted, user_id)
            )
            await db.commit()
    
    async def increment_ai_requests(self, user_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "UPDATE users SET ai_requests = ai_requests + 1 WHERE user_id = ?",
                (user_id,)
            )
            await db.commit()
    
    async def get_user(self, user_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
                return await cursor.fetchone()
    
    async def get_all_users(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT COUNT(*) FROM users") as cursor:
                result = await cursor.fetchone()
                return result[0] if result else 0
    
    async def get_active_users_count(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT COUNT(*) FROM users WHERE last_active > datetime('now', '-7 days')") as cursor:
                result = await cursor.fetchone()
                return result[0] if result else 0
    
    async def get_user_ids(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT user_id FROM users WHERE is_banned = 0") as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]
    
    async def get_all_users_data(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT user_id, username, full_name, registration_date FROM users ORDER BY registration_date DESC LIMIT 100") as cursor:
                return await cursor.fetchall()
    
    async def ban_user(self, user_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("UPDATE users SET is_banned = 1 WHERE user_id = ?", (user_id,))
            await db.commit()
    
    async def unban_user(self, user_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("UPDATE users SET is_banned = 0 WHERE user_id = ?", (user_id,))
            await db.commit()
    
    async def add_admin_channel(self, channel_username: str, channel_title: str, channel_link: str, added_by: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                """INSERT OR REPLACE INTO admin_channels 
                (channel_username, channel_title, channel_link, added_by) 
                VALUES (?, ?, ?, ?)""",
                (channel_username, channel_title, channel_link, added_by)
            )
            await db.commit()
    
    async def get_admin_channels(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT * FROM admin_channels ORDER BY id") as cursor:
                return await cursor.fetchall()
    
    async def delete_admin_channel(self, channel_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("DELETE FROM admin_channels WHERE id = ?", (channel_id,))
            await db.commit()
    
    async def add_private_channel(self, name: str, link: str, added_by: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                """INSERT OR IGNORE INTO private_channels 
                (name, link, added_by) 
                VALUES (?, ?, ?)""",
                (name, link, added_by)
            )
            await db.commit()
    
    async def get_private_channels(self, limit: int = 200):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT * FROM private_channels ORDER BY id LIMIT ?", (limit,)) as cursor:
                return await cursor.fetchall()
    
    async def delete_private_channel(self, channel_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("DELETE FROM private_channels WHERE id = ?", (channel_id,))
            await db.commit()
    
    async def add_admin(self, user_id: int, username: str, added_by: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                """INSERT OR IGNORE INTO admins 
                (user_id, username, added_by) 
                VALUES (?, ?, ?)""",
                (user_id, username, added_by)
            )
            await db.commit()
    
    async def get_admins(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT * FROM admins") as cursor:
                return await cursor.fetchall()
    
    async def is_admin(self, user_id: int):
        if user_id in ADMIN_IDS:
            return True
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT 1 FROM admins WHERE user_id = ?", (user_id,)) as cursor:
                return await cursor.fetchone() is not None
    
    async def remove_admin(self, user_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("DELETE FROM admins WHERE user_id = ? AND user_id != ?", (user_id, OWNER_ID))
            await db.commit()
    
    async def update_stat(self, metric: str, value: int = 1):
        async with aiosqlite.connect(self.db_name) as db:
            # Сначала проверяем, существует ли запись
            cursor = await db.execute("SELECT 1 FROM stats WHERE metric = ?", (metric,))
            exists = await cursor.fetchone()
            
            if exists:
                await db.execute(
                    "UPDATE stats SET value = value + ?, updated_date = CURRENT_TIMESTAMP WHERE metric = ?",
                    (value, metric)
                )
            else:
                await db.execute(
                    "INSERT INTO stats (metric, value) VALUES (?, ?)",
                    (metric, value)
                )
            await db.commit()
    
    async def get_stat(self, metric: str):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT value FROM stats WHERE metric = ?", (metric,)) as cursor:
                result = await cursor.fetchone()
                return result[0] if result and result[0] else 0

# Инициализация базы данных
db = Database()

# Вспомогательные функции
async def check_subscription(user_id: int, channel_username: str) -> bool:
    """Проверяет, подписан ли пользователь на канал"""
    try:
        member = await bot.get_chat_member(chat_id=channel_username, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.error(f"Ошибка проверки подписки: {e}")
        return False

def generate_captcha() -> tuple:
    """Генерирует случайную капчу"""
    num1 = random.randint(1, 15)
    num2 = random.randint(1, 15)
    operation = random.choice(['+', '-', '*'])
    
    if operation == '+':
        answer = num1 + num2
    elif operation == '-':
        answer = num1 - num2
    else:
        answer = num1 * num2
    
    question = f"{num1} {operation} {num2} = ?"
    return question, str(answer)

# УПРОЩЕННАЯ НЕЙРОСЕТЬ С ПОИСКОМ В ИНТЕРНЕТЕ (без сложных зависимостей)
async def ai_search_internet(question: str) -> str:
    """Ищет информацию в интернете через простые API"""
    try:
        # Используем простой API для поиска (DuckDuckGo Instant Answer)
        search_url = f"https://api.duckduckgo.com/?q={question}&format=json&no_html=1"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get('AbstractText'):
                        abstract = data['AbstractText']
                        source = data.get('AbstractSource', 'DuckDuckGo')
                        url = data.get('AbstractURL', '')
                        
                        response_text = f"🤖 *AI:* Вот что я нашел:\n\n"
                        response_text += f"{abstract}\n\n"
                        if url:
                            response_text += f"🔗 *Источник:* {source}\n{url}"
                        return response_text
                    
                    elif data.get('RelatedTopics'):
                        topics = data['RelatedTopics'][:3]
                        response_text = "🤖 *AI:* Вот что я нашел по вашему запросу:\n\n"
                        
                        for i, topic in enumerate(topics, 1):
                            if isinstance(topic, dict) and 'Text' in topic:
                                text = topic['Text']
                                response_text += f"{i}. {text}\n\n"
                        
                        return response_text
        
        # Если не нашли через API, возвращаем умный ответ
        return ai_smart_response(question)
        
    except Exception as e:
        logger.error(f"Ошибка AI поиска: {e}")
        return ai_smart_response(question)

def ai_smart_response(question: str) -> str:
    """Генерирует умный ответ на основе ключевых слов"""
    question_lower = question.lower()
    
    # Ответы на популярные вопросы
    responses = [
        "🤖 *AI:* На основе доступной информации могу сказать, что ",
        "🤖 *AI:* Согласно моим данным, ",
        "🤖 *AI:* По этому вопросу существует следующая информация: ",
    ]
    
    base_response = random.choice(responses)
    
    # Проверяем ключевые слова
    if any(word in question_lower for word in ['привет', 'здравствуй', 'hello', 'hi']):
        return "🤖 *AI:* Привет! Я ваш AI помощник. Задавайте вопросы, и я постараюсь найти информацию в интернете!"
    
    elif any(word in question_lower for word in ['как дела', 'как ты', 'настроение']):
        return "🤖 *AI:* Спасибо за вопрос! Я функционирую нормально и готов помогать. Чем могу быть полезен?"
    
    elif any(word in question_lower for word in ['погода', 'температура', 'дождь']):
        return "🌤 *AI:* К сожалению, у меня нет доступа к актуальным данным о погоде. Рекомендую использовать специализированные погодные сервисы или приложения."
    
    elif any(word in question_lower for word in ['время', 'дата', 'который час']):
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%d.%m.%Y")
        return f"⏰ *AI:* Сейчас {current_time}, {current_date}"
    
    elif any(word in question_lower for word in ['python', 'программирование', 'код']):
        return f"{base_response}Python - это популярный язык программирования. Он широко используется в веб-разработке, data science, искусственном интеллекте и автоматизации."
    
    elif any(word in question_lower for word in ['бот', 'телеграм', 'telegram']):
        return f"{base_response}Telegram боты создаются с помощью Telegram Bot API. Для создания ботов используется язык программирования Python с библиотекой aiogram."
    
    elif any(word in question_lower for word in ['ии', 'нейросеть', 'искусственный интеллект']):
        return f"{base_response}Искусственный интеллект (ИИ) - это область компьютерных наук, занимающаяся созданием интеллектуальных машин. Нейросети - один из подходов в ИИ."
    
    else:
        # Общий ответ
        return f"{base_response}это интересный вопрос. Рекомендую поискать дополнительную информацию в интернете или специализированных источниках."

def create_main_menu() -> ReplyKeyboardMarkup:
    """Создает главное меню"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎮 Мини-игры"), KeyboardButton(text="🔗 Приватки")],
            [KeyboardButton(text="🤖 Нейросеть"), KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="📜 Правила"), KeyboardButton(text="❓ Помощь")],
        ],
        resize_keyboard=True
    )
    return keyboard

def create_admin_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру админ-панели"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
            [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")],
            [InlineKeyboardButton(text="➕ Канал", callback_data="admin_add_channel")],
            [InlineKeyboardButton(text="🗑 Канал", callback_data="admin_remove_channel")],
            [InlineKeyboardButton(text="➕ Приват", callback_data="admin_add_private")],
            [InlineKeyboardButton(text="🗑 Приват", callback_data="admin_remove_private")],
            [InlineKeyboardButton(text="👑 Админы", callback_data="admin_manage")],
            [InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast")],
            [InlineKeyboardButton(text="⛔ Бан", callback_data="admin_ban")],
            [InlineKeyboardButton(text="✅ Разбан", callback_data="admin_unban")],
            [InlineKeyboardButton(text="🔙 Выход", callback_data="admin_back")]
        ]
    )
    return keyboard

def create_games_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру мини-игр"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎲 Кубик", callback_data="game_dice")],
            [InlineKeyboardButton(text="🎯 Дротик", callback_data="game_dart")],
            [InlineKeyboardButton(text="🏀 Баскетбол", callback_data="game_basketball")],
            [InlineKeyboardButton(text="⚽ Футбол", callback_data="game_football")],
            [InlineKeyboardButton(text="🎰 Слоты", callback_data="game_slot")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="game_back")]
        ]
    )
    return keyboard

def create_ai_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для нейросети"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔍 Задать вопрос", callback_data="ai_question")],
            [InlineKeyboardButton(text="📊 Моя статистика", callback_data="ai_stats")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="ai_back")]
        ]
    )
    return keyboard

# Обработчики команд
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    username = message.from_user.username or ""
    full_name = message.from_user.full_name
    
    await db.add_user(user_id, username, full_name)
    await db.update_stat("starts")
    
    # Проверяем бан
    user_data = await db.get_user(user_id)
    if user_data and len(user_data) > 9 and user_data[9]:
        await message.answer("⛔ *Вы забанены в этом боте!*", parse_mode="Markdown")
        return
    
    welcome_text = f"""
✨ *Добро пожаловать, {full_name}!*

🤖 *Я - многофункциональный бот:*
• 🎮 Мини-игры
• 🔗 50+ приватных каналов
• 🤖 Нейросеть с поиском
• 📊 Статистика

👇 *Для доступа пройдите быструю регистрацию*
    """
    
    await message.answer(welcome_text, parse_mode="Markdown")
    
    # Проверяем регистрацию
    if user_data and user_data[3] and user_data[4] and user_data[5]:
        await message.answer("✅ *Вы уже зарегистрированы!*", reply_markup=create_main_menu())
        await state.clear()
        return
    
    if not user_data or not user_data[3]:
        await show_captcha(message, state)
    elif not user_data[4]:
        await check_all_subscriptions(message, state)
    elif not user_data[5]:
        await show_rules(message, state)

async def show_captcha(message: types.Message, state: FSMContext):
    """Показывает капчу"""
    question, answer = generate_captcha()
    
    await state.set_state(UserState.waiting_captcha)
    await state.update_data(captcha_answer=answer)
    
    await message.answer(f"🔐 *Решите пример:*\n\n`{question}`\n\n*Введите ответ:*", parse_mode="Markdown")

@dp.message(UserState.waiting_captcha)
async def process_captcha(message: types.Message, state: FSMContext):
    """Обрабатывает ответ на капчу"""
    user_answer = message.text.strip()
    data = await state.get_data()
    correct_answer = data.get("captcha_answer")
    
    if user_answer == correct_answer:
        await db.update_user_captcha(message.from_user.id)
        await db.update_stat("captcha_passed")
        await message.answer("✅ *Капча пройдена!*", parse_mode="Markdown")
        await check_all_subscriptions(message, state)
    else:
        await message.answer("❌ *Неверно! Попробуйте снова.*", parse_mode="Markdown")
        await show_captcha(message, state)

async def check_all_subscriptions(message: types.Message, state: FSMContext):
    """Проверяет подписки на каналы"""
    # Все каналы: обязательные + из базы
    all_channels = REQUIRED_CHANNELS.copy()
    admin_channels = await db.get_admin_channels()
    
    for channel in admin_channels:
        all_channels.append({
            "username": channel[1],
            "title": channel[2] or channel[1],
            "link": channel[3]
        })
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    text = "📢 *Подпишитесь на каналы:*\n\n"
    
    for channel in all_channels:
        text += f"• {channel['title']}\n"
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text=f"📢 {channel['title'][:20]}", url=channel['link'])
        ])
    
    text += "\n*После подписки нажмите:*"
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="✅ Проверить", callback_data="check_subscription")])
    
    await state.set_state(UserState.waiting_subscription)
    await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)

@dp.callback_query(F.data == "check_subscription")
async def verify_subscription(callback: CallbackQuery, state: FSMContext):
    """Проверяет подписки"""
    user_id = callback.from_user.id
    all_channels = REQUIRED_CHANNELS.copy()
    admin_channels = await db.get_admin_channels()
    
    for channel in admin_channels:
        all_channels.append({
            "username": channel[1],
            "title": channel[2] or channel[1],
            "link": channel[3]
        })
    
    not_subscribed = []
    for channel in all_channels:
        if not await check_subscription(user_id, channel["username"]):
            not_subscribed.append(channel["title"])
    
    if not not_subscribed:
        await db.update_user_subscription(user_id)
        await db.update_stat("subscribed")
        await callback.message.edit_text("✅ *Все подписки подтверждены!*", parse_mode="Markdown")
        await show_rules(callback.message, state)
    else:
        await callback.answer(f"❌ Не подписан на: {', '.join(not_subscribed)}", show_alert=True)
    
    await callback.answer()

async def show_rules(message: types.Message, state: FSMContext):
    """Показывает правила"""
    rules_text = f"""
📜 *Правила бота:*

1. 🤝 Уважайте других
2. 📢 Не спамьте
3. 🔗 Подпишитесь на каналы
4. 🤖 Используйте AI ответственно
5. 📞 Помощь: {OWNER_USERNAME}

*Нажмите "Принять":*
    """
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Принять правила", callback_data="accept_rules")]
    ])
    
    await state.set_state(UserState.reading_rules)
    await message.answer(rules_text, parse_mode="Markdown", reply_markup=keyboard)

@dp.callback_query(F.data == "accept_rules")
async def accept_rules(callback: CallbackQuery, state: FSMContext):
    """Принимает правила"""
    await db.update_user_rules(callback.from_user.id)
    await db.update_stat("rules_accepted")
    
    await callback.message.edit_text(f"🎉 *Регистрация завершена, {callback.from_user.full_name}!*", parse_mode="Markdown")
    await callback.message.answer("👇 *Главное меню:*", reply_markup=create_main_menu())
    await state.clear()
    await callback.answer()

# Основные функции
@dp.message(F.text == "🎮 Мини-игры")
async def show_games(message: types.Message):
    """Показывает игры"""
    user_data = await db.get_user(message.from_user.id)
    if not user_data or not (user_data[3] and user_data[4] and user_data[5]):
        await message.answer("⚠️ *Сначала пройдите регистрацию!*", parse_mode="Markdown")
        return
    
    await message.answer("🎮 *Выберите игру:*", reply_markup=create_games_keyboard())

@dp.message(F.text == "🔗 Приватки")
async def send_private_links(message: types.Message):
    """Отправляет приватки"""
    user_data = await db.get_user(message.from_user.id)
    if not user_data or not (user_data[3] and user_data[4] and user_data[5]):
        await message.answer("⚠️ *Сначала пройдите регистрацию!*", parse_mode="Markdown")
        return
    
    private_channels = await db.get_private_channels()
    
    await message.answer(f"🔗 *Всего приватных каналов: {len(private_channels)}*", parse_mode="Markdown")
    
    # Отправляем частями
    for i in range(0, len(private_channels), 10):
        chunk = private_channels[i:i+10]
        text = ""
        for channel in chunk:
            name = channel[1] or f"Приват #{channel[0]}"
            link = channel[2]
            text += f"{name}\n{link}\n\n"
        
        await message.answer(text, disable_web_page_preview=True)
        await asyncio.sleep(0.5)

@dp.message(F.text == "🤖 Нейросеть")
async def show_ai_menu(message: types.Message):
    """Показывает AI меню"""
    user_data = await db.get_user(message.from_user.id)
    if not user_data or not (user_data[3] and user_data[4] and user_data[5]):
        await message.answer("⚠️ *Сначала пройдите регистрацию!*", parse_mode="Markdown")
        return
    
    await message.answer("🤖 *AI помощник с поиском в интернете*", reply_markup=create_ai_keyboard())

@dp.message(F.text == "📊 Статистика")
async def show_stats(message: types.Message):
    """Показывает статистику"""
    user_data = await db.get_user(message.from_user.id)
    if not user_data or not (user_data[3] and user_data[4] and user_data[5]):
        await message.answer("⚠️ *Сначала пройдите регистрацию!*", parse_mode="Markdown")
        return
    
    total_users = await db.get_all_users()
    ai_requests = user_data[8] if len(user_data) > 8 else 0
    
    text = f"""
📊 *Ваша статистика:*

👤 ID: `{user_data[0]}`
📛 Имя: {user_data[2]}
📅 Регистрация: {user_data[6][:10] if user_data[6] else 'Нет'}

🤖 Запросов к AI: {ai_requests}
👥 Всего пользователей: {total_users}
    """
    
    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text == "📜 Правила")
async def show_rules_menu(message: types.Message):
    """Показывает правила"""
    await message.answer(f"📜 *Правила бота:*\n\n1. Уважайте других\n2. Не спамьте\n3. Подпишитесь на каналы\n4. Помощь: {OWNER_USERNAME}", parse_mode="Markdown")

@dp.message(F.text == "❓ Помощь")
async def show_help_menu(message: types.Message):
    """Показывает помощь"""
    text = f"""
❓ *Помощь:*

🤖 *Команды:*
• /start - запуск бота
• /admin - админ-панель

🔗 *Обязательные каналы:*
1. Manuals and softs🔫
2. Чат зайса)

📞 *Контакты:*
{OWNER_USERNAME}
ID: `{OWNER_ID}`
    """
    await message.answer(text, parse_mode="Markdown")

# Обработчики игр
@dp.callback_query(F.data.startswith("game_"))
async def process_game(callback: CallbackQuery):
    """Обрабатывает игры"""
    game = callback.data.split("_")[1]
    
    if game == "back":
        await callback.message.delete()
    elif game == "dice":
        await callback.message.answer_dice(emoji="🎲")
    elif game == "dart":
        await callback.message.answer_dice(emoji="🎯")
    elif game == "basketball":
        await callback.message.answer_dice(emoji="🏀")
    elif game == "football":
        await callback.message.answer_dice(emoji="⚽")
    elif game == "slot":
        await callback.message.answer_dice(emoji="🎰")
    
    await callback.answer()

# Обработчики AI
@dp.callback_query(F.data.startswith("ai_"))
async def process_ai(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает AI"""
    action = callback.data.split("_")[1]
    
    if action == "back":
        await callback.message.delete()
    elif action == "question":
        await callback.message.answer("🤖 *Задайте вопрос для поиска в интернете:*", parse_mode="Markdown")
        await state.set_state(UserState.ai_waiting_question)
    elif action == "stats":
        user_data = await db.get_user(callback.from_user.id)
        if user_data:
            ai_requests = user_data[8] if len(user_data) > 8 else 0
            await callback.message.edit_text(f"📊 *Ваши запросы к AI:* {ai_requests}", parse_mode="Markdown")
    
    await callback.answer()

@dp.message(UserState.ai_waiting_question)
async def process_ai_question(message: types.Message, state: FSMContext):
    """Обрабатывает вопрос AI"""
    if len(message.text) < 3:
        await message.answer("❌ *Вопрос слишком короткий*", parse_mode="Markdown")
        return
    
    # Показываем поиск
    search_msg = await message.answer("🔍 *Ищу информацию...*", parse_mode="Markdown")
    
    # Ищем ответ
    response = await ai_search_internet(message.text)
    
    # Увеличиваем счетчик
    await db.increment_ai_requests(message.from_user.id)
    await db.update_stat("ai_requests")
    
    # Удаляем сообщение поиска и отправляем ответ
    await search_msg.delete()
    await message.answer(response, parse_mode="Markdown")
    
    await state.clear()

# АДМИН-ПАНЕЛЬ
@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    """Админ-панель"""
    if not await db.is_admin(message.from_user.id):
        await message.answer("⛔ *Нет доступа!*", parse_mode="Markdown")
        return
    
    await message.answer("👑 *Админ-панель:*", reply_markup=create_admin_keyboard())

@dp.callback_query(F.data.startswith("admin_"))
async def process_admin(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает админ-действия"""
    if not await db.is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа!", show_alert=True)
        return
    
    action = callback.data.split("_")[1]
    
    if action == "back":
        await callback.message.delete()
    
    elif action == "stats":
        await show_admin_stats(callback)
    
    elif action == "users":
        await show_admin_users(callback)
    
    elif action == "add_channel":
        await callback.message.answer("📝 Введите @username канала:")
        await state.set_state(AdminState.waiting_channel_username)
    
    elif action == "remove_channel":
        await show_channels_list(callback)
    
    elif action == "add_private":
        await callback.message.answer("📝 Введите название приватного канала:")
        await state.set_state(AdminState.waiting_private_name)
    
    elif action == "remove_private":
        await show_privates_list(callback)
    
    elif action == "manage":
        await show_admins_list(callback)
    
    elif action == "broadcast":
        await callback.message.answer("📢 Введите сообщение для рассылки:")
        await state.set_state(AdminState.waiting_broadcast)
    
    elif action == "ban":
        await callback.message.answer("⛔ Введите ID пользователя для бана:")
        await state.set_state(AdminState.waiting_user_id)
        await state.update_data(action="ban")
    
    elif action == "unban":
        await callback.message.answer("✅ Введите ID пользователя для разбана:")
        await state.set_state(AdminState.waiting_user_id)
        await state.update_data(action="unban")
    
    await callback.answer()

async def show_admin_stats(callback: CallbackQuery):
    """Показывает статистику админа"""
    total_users = await db.get_all_users()
    active_users = await db.get_active_users_count()
    captcha = await db.get_stat("captcha_passed")
    subscribed = await db.get_stat("subscribed")
    rules = await db.get_stat("rules_accepted")
    starts = await db.get_stat("starts")
    ai_requests = await db.get_stat("ai_requests")
    
    admin_channels = await db.get_admin_channels()
    private_channels = await db.get_private_channels()
    
    text = f"""
📊 *Статистика бота:*

👥 Пользователи: {total_users}
📈 Активные: {active_users}
✅ Капча: {captcha}
📢 Подписки: {subscribed}
📜 Правила: {rules}
🚀 Стартов: {starts}
🤖 AI запросов: {ai_requests}

📢 Каналов: {len(admin_channels)}
🔗 Приваток: {len(private_channels)}
    """
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Обновить", callback_data="admin_stats")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
    ])
    
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=keyboard)

async def show_admin_users(callback: CallbackQuery):
    """Показывает пользователей"""
    users = await db.get_all_users_data()
    
    text = "👥 *Последние пользователи:*\n\n"
    for user in users[:10]:
        text += f"ID: `{user[0]}`\nИмя: {user[2]}\n\n"
    
    if len(users) > 10:
        text += f"... и еще {len(users) - 10} пользователей"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
    ])
    
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=keyboard)

async def show_channels_list(callback: CallbackQuery):
    """Показывает каналы для удаления"""
    channels = await db.get_admin_channels()
    
    if not channels:
        await callback.answer("❌ Нет каналов!", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for channel in channels:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"🗑 {channel[2] or channel[1]}",
                callback_data=f"delete_channel_{channel[0]}"
            )
        ])
    
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")])
    
    await callback.message.edit_text("🗑 *Выберите канал:*", reply_markup=keyboard)

async def show_privates_list(callback: CallbackQuery):
    """Показывает приватки для удаления"""
    privates = await db.get_private_channels(limit=20)
    
    if not privates:
        await callback.answer("❌ Нет приваток!", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for private_ch in privates:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"🗑 {private_ch[1] or f'Приват #{private_ch[0]}'}",
                callback_data=f"delete_private_{private_ch[0]}"
            )
        ])
    
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")])
    
    await callback.message.edit_text("🗑 *Выберите приватный канал:*", reply_markup=keyboard)

async def show_admins_list(callback: CallbackQuery):
    """Показывает админов"""
    admins = await db.get_admins()
    
    text = "👑 *Администраторы:*\n\n"
    for admin in admins:
        if admin[0] != OWNER_ID:
            text += f"ID: `{admin[0]}`\n@{admin[1]}\n\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить", callback_data="admin_add_admin")],
        [InlineKeyboardButton(text="🗑 Удалить", callback_data="admin_remove_admin")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
    ])
    
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=keyboard)

# Удаление каналов/приваток
@dp.callback_query(F.data.startswith("delete_"))
async def delete_item(callback: CallbackQuery):
    """Удаляет канал или приват"""
    if not await db.is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа!", show_alert=True)
        return
    
    data = callback.data.split("_")
    type_ = data[1]
    id_ = int(data[2])
    
    if type_ == "channel":
        await db.delete_admin_channel(id_)
        await callback.answer("✅ Канал удален!", show_alert=True)
        await show_channels_list(callback)
    elif type_ == "private":
        await db.delete_private_channel(id_)
        await callback.answer("✅ Приват удален!", show_alert=True)
        await show_privates_list(callback)

# Обработка состояний админа
@dp.message(AdminState.waiting_channel_username)
async def process_admin_channel_username(message: types.Message, state: FSMContext):
    """Обрабатывает username канала"""
    username = message.text.strip()
    if not username.startswith('@'):
        username = '@' + username
    
    await state.update_data(channel_username=username)
    await message.answer("📝 Теперь введите ссылку на канал:")
    await state.set_state(AdminState.waiting_channel_link)

@dp.message(AdminState.waiting_channel_link)
async def process_admin_channel_link(message: types.Message, state: FSMContext):
    """Обрабатывает ссылку канала"""
    data = await state.get_data()
    username = data.get('channel_username')
    link = message.text.strip()
    
    await db.add_admin_channel(username, username, link, message.from_user.id)
    await message.answer(f"✅ Канал {username} добавлен!")
    await state.clear()

@dp.message(AdminState.waiting_private_name)
async def process_admin_private_name(message: types.Message, state: FSMContext):
    """Обрабатывает название приватного канала"""
    name = message.text.strip()
    await state.update_data(private_name=name)
    await message.answer("📝 Теперь введите ссылку на приватный канал:")
    await state.set_state(AdminState.waiting_private_link)

@dp.message(AdminState.waiting_private_link)
async def process_admin_private_link(message: types.Message, state: FSMContext):
    """Обрабатывает ссылку приватного канала"""
    data = await state.get_data()
    name = data.get('private_name')
    link = message.text.strip()
    
    await db.add_private_channel(name, link, message.from_user.id)
    await message.answer(f"✅ Приват {name} добавлен!")
    await state.clear()

@dp.message(AdminState.waiting_user_id)
async def process_admin_user_id(message: types.Message, state: FSMContext):
    """Обрабатывает ID пользователя для бана/разбана"""
    data = await state.get_data()
    action = data.get('action')
    
    try:
        user_id = int(message.text.strip())
        
        if action == "ban":
            await db.ban_user(user_id)
            await message.answer(f"⛔ Пользователь {user_id} забанен!")
        elif action == "unban":
            await db.unban_user(user_id)
            await message.answer(f"✅ Пользователь {user_id} разбанен!")
    
    except ValueError:
        await message.answer("❌ Ошибка: Введите числовой ID")
    
    await state.clear()

@dp.message(AdminState.waiting_broadcast)
async def process_admin_broadcast(message: types.Message, state: FSMContext):
    """Обрабатывает рассылку"""
    text = message.text
    user_ids = await db.get_user_ids()
    
    if not user_ids:
        await message.answer("❌ Нет пользователей для рассылки!")
        await state.clear()
        return
    
    await message.answer(f"📢 Рассылаю {len(user_ids)} пользователям...")
    
    sent = 0
    failed = 0
    
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, text)
            sent += 1
            await asyncio.sleep(0.1)
        except:
            failed += 1
    
    await message.answer(f"✅ Рассылка завершена!\n\n✅ Отправлено: {sent}\n❌ Ошибок: {failed}")
    await state.clear()

# Добавление/удаление админов
@dp.callback_query(F.data == "admin_add_admin")
async def add_admin_callback(callback: CallbackQuery, state: FSMContext):
    """Добавление админа"""
    await callback.message.answer("👑 Введите ID пользователя для добавления в админы:")
    await state.set_state(AdminState.waiting_admin_id)
    await state.update_data(action="add_admin")
    await callback.answer()

@dp.callback_query(F.data == "admin_remove_admin")
async def remove_admin_callback(callback: CallbackQuery):
    """Удаление админа"""
    admins = await db.get_admins()
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for admin in admins:
        if admin[0] != OWNER_ID:
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text=f"🗑 {admin[1] or f'ID {admin[0]}'}",
                    callback_data=f"remove_admin_{admin[0]}"
                )
            ])
    
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")])
    
    await callback.message.edit_text("🗑 *Выберите админа для удаления:*", reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(F.data.startswith("remove_admin_"))
async def remove_admin_process(callback: CallbackQuery):
    """Удаляет админа"""
    admin_id = int(callback.data.split("_")[2])
    
    if admin_id == OWNER_ID:
        await callback.answer("❌ Нельзя удалить владельца!", show_alert=True)
        return
    
    await db.remove_admin(admin_id)
    await callback.answer("✅ Админ удален!", show_alert=True)
    await show_admins_list(callback)

@dp.message(AdminState.waiting_admin_id)
async def process_admin_admin_id(message: types.Message, state: FSMContext):
    """Обрабатывает ID админа"""
    data = await state.get_data()
    action = data.get('action')
    
    try:
        user_id = int(message.text.strip())
        
        if action == "add_admin":
            try:
                user = await bot.get_chat(user_id)
                username = user.username or f"ID {user_id}"
                await db.add_admin(user_id, username, message.from_user.id)
                await message.answer(f"✅ Админ {username} добавлен!")
            except Exception as e:
                await message.answer(f"❌ Ошибка: {e}")
    
    except ValueError:
        await message.answer("❌ Ошибка: Введите числовой ID")
    
    await state.clear()

# Основная функция
async def main():
    """Запуск бота"""
    logger.info("🚀 Запускаю бота...")
    
    # Инициализируем базу
    await db.init_db()
    
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())