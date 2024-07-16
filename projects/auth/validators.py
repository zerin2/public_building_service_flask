from dataclasses import dataclass, field
from typing import Type
from string import digits, ascii_letters

from werkzeug.security import check_password_hash, generate_password_hash

from logs.logs_config import auth_logger
from projects.auth.config import SPECIAL_CHARACTERS, CYRILLIC, ERROR_MESSAGES
from projects.auth.models import User, Departments
from settings import AUTH_ACCESS_CODE


@dataclass
class ValidationForm:
    name: str = ''
    surname: str = ''
    email: str = ''
    password: str = ''
    password_repeat: str = ''
    department_id: str = ''
    access_code: str = ''
    errors: dict = field(default_factory=dict)

    def validate_email(self) -> bool:
        if self.email is None or self.email == '':
            self.errors['error_email'] = ERROR_MESSAGES['error_email']['empty']
        if len(self.email) < 5:
            self.errors['error_email'] = ERROR_MESSAGES['error_email']['incorrect_length']
        elif '@' not in self.email or '.' not in self.email:
            self.errors['error_email'] = ERROR_MESSAGES['error_email']['incorrect_format']
        elif any(char in CYRILLIC for char in self.email):
            self.errors['error_email'] = ERROR_MESSAGES['error_email']['incorrect_format']
        elif not any(char in self.email for char in ascii_letters):
            self.errors['error_email'] = ERROR_MESSAGES['error_email']['incorrect_format']

    def validate_name(self) -> bool:
        if self.name is None or self.name == '':
            self.errors['error_name'] = ERROR_MESSAGES['error_name']['empty']
        if len(self.name) < 2:
            self.errors['error_name'] = ERROR_MESSAGES['error_name']['incorrect_length']
        elif any(char in ascii_letters for char in self.name):
            self.errors['error_name'] = ERROR_MESSAGES['error_name']['incorrect_characters']
        elif any(char in digits for char in self.name):
            self.errors['error_name'] = ERROR_MESSAGES['error_name']['incorrect_characters']
        elif any(char in SPECIAL_CHARACTERS for char in self.name):
            self.errors['error_name'] = ERROR_MESSAGES['error_name']['incorrect_characters_spec']

    def validate_surname(self) -> bool:
        if self.surname is None or self.surname == '':
            self.errors['error_surname'] = ERROR_MESSAGES['error_surname']['empty']
        if len(self.surname) < 2:
            self.errors['error_surname'] = ERROR_MESSAGES['error_surname']['incorrect_length']
        elif any(char in ascii_letters for char in self.surname):
            self.errors['error_surname'] = ERROR_MESSAGES['error_surname']['incorrect_characters']
        elif any(char in digits for char in self.surname):
            self.errors['error_surname'] = ERROR_MESSAGES['error_surname']['incorrect_characters']
        elif any(char in SPECIAL_CHARACTERS for char in self.surname):
            self.errors['error_surname'] = ERROR_MESSAGES['error_surname']['incorrect_characters_spec']

    def validate_password(self) -> bool:
        if self.password is None or self.password == '':
            self.errors['error_password'] = ERROR_MESSAGES['error_password']['empty']
        if len(self.password) < 8:
            self.errors['error_password'] = ERROR_MESSAGES['error_password']['incorrect_length']
        elif any(char in CYRILLIC for char in self.password):
            self.errors['error_password'] = ERROR_MESSAGES['error_password']['incorrect_characters']
        elif not any(char in self.password for char in ascii_letters):
            self.errors['error_password'] = ERROR_MESSAGES['error_password']['incorrect_format']

    def validate_password_repeat(self) -> bool:
        if self.password != self.password_repeat:
            self.errors['error_password_repeat'] = ERROR_MESSAGES['error_password_repeat']['mismatch']

    def validate_department_id(self) -> bool:
        departments = (Departments.select(Departments.id))
        department_list = [str(department.id) for department in departments]
        if self.department_id not in department_list:
            self.errors['error_department_id'] = ERROR_MESSAGES['error_department_id']['incorrect']

    def validate_access_code(self) -> bool:
        if self.access_code is None or self.access_code == '':
            self.errors['error_access_code'] = ERROR_MESSAGES['error_access_code']['incorrect_code']
        if self.access_code not in AUTH_ACCESS_CODE:
            self.errors['error_access_code'] = ERROR_MESSAGES['error_access_code']['incorrect_code']


@dataclass
class UserAuth(ValidationForm):
    errors: dict = field(default_factory=dict)

    def validate(self) -> [bool, dict]:
        self.validate_email()
        self.validate_name()
        self.validate_surname()
        self.validate_password()
        self.validate_password_repeat()
        self.validate_department_id()
        self.validate_access_code()

        if self.errors:
            auth_logger.info(
                f'Неудачная регистрация пользователя {self.email}. '
                f'Ошибки: {self.errors}'
            )
            return False, self.errors
        else:
            auth_logger.info(f'Удачная регистрация пользователя {self.email}.')
            return True, self.errors

    def authenticate_user(self):
        """
        Проверяет аутентификацию пользователя по email и паролю.
        Возвращает пользователя, если аутентификация успешна, иначе возвращает False.
        """
        try:
            user = User.get(User.email == self.email)
        except Exception as e:
            auth_logger.error(f'Ошибка аутентификации: {e}.')
            return False
        else:
            user_password_hash = user.password
            if check_password_hash(user_password_hash, self.password):
                auth_logger.info(f'Успешная аутентификация {self.email}.')
                return user
            else:
                return False

    def save_user(self) -> None:
        """
        Сохраняет данные пользователя в базу данных.
        Хэширует пароль перед сохранением.
        """
        self.password = generate_password_hash(self.password)
        try:
            User.insert_many(
                [(
                    self.name,
                    self.surname,
                    self.email,
                    self.password,
                    int(self.department_id),
                )],
                fields=[
                    User.name,
                    User.surname,
                    User.email,
                    User.password,
                    User.department,
                ]
            ).execute()
            auth_logger.info(f'Удачное сохранения пользователя {self.email} в бд.')
        except Exception as e:
            auth_logger.error(f'Ошибка сохранения пользователя: {e} в бд.')

    def check_email_exists(self) -> bool:
        """
        Проверяет, существует ли пользователь с заданным email.
        Возвращает True, если пользователь найден,
        иначе добавляет ошибку в self.errors и возвращает False.
        """
        try:
            User.get(User.email == self.email)
        except User.DoesNotExist:
            auth_logger.info(f'Пользователя {self.email} нет в бд.')
            self.errors['error_email'] = ERROR_MESSAGES['error_email']['no_find']
            return False
        else:
            return True


@dataclass
class PasswordRecovery(UserAuth):
    errors: dict = field(default_factory=dict)

    def validate_recovery_email(self) -> [bool, dict]:
        self.validate_email()
        self.check_email_exists()
        if self.errors:
            return False, self.errors
        else:
            auth_logger.info(f'Успешная отправка сброса пароля {self.email}.')
            return True, self.errors
