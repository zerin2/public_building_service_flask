import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

"""Папка проекта."""
ROOT_DIRECTORY = os.getenv('ROOT_DIRECTORY')

"""Ключи."""
APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')
AUTH_ACCESS_CODE = os.getenv('AUTH_ACCESS_CODE')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USER = os.getenv('DB_USER')

"""Сессии."""
SESSION_KEY_USER_ID = 'user_id'
SESSION_KEY_ROLE_NAME = 'role_name'
SESSION_LIFETIME = 1_209_600  # (sec) = 14 days
SESSION_PERMANENT_VALUE = True

"""Тестовый путь и значение."""
EXCEL = Path(__file__).resolve().parent / 'uploads' / 'test_registry.xls'

"""Путь сохранения файла."""
UPLOAD_FOLDER: str = 'uploads/'

"""Допустимые разрешения файла банка."""
ALLOWED_EXTENSIONS_BANK: list[str] = [
    '.xls',
    '.xlm',
    '.xlt',
    '.xlsx',
    '.xlsm',
    '.xltx',
    '.xltm',
]

"""Допустимые размер файла банка."""
MAX_SIZE_BANK: int = 1024 * 1024 * 10

"""Допустимый размер файла для загрузки на сайт."""
MAX_FILE_UPLOAD_SIZE: int = 1024 * 1024 * 30
