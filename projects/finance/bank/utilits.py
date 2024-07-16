import os
import datetime as dt
from typing import NoReturn
from dataclasses import dataclass

from werkzeug.utils import secure_filename

from projects.auth.config import ERROR_MESSAGES


@dataclass
class FileValidation:
    uploaded_file: object
    allowed_extensions: list[str]
    max_size: int

    def __post_init__(self):
        """Сохранение имени в безопасном формате."""
        self.file_name = secure_filename(self.uploaded_file.filename)

    def validate(self) -> [bool, dict]:
        self.errors = {}
        self.validate_filename()
        self.validate_extension()
        self.validate_size()
        if self.errors:
            return False, self.errors
        else:
            return True, self.errors

    def validate_filename(self) -> bool:
        if self.file_name == '':
            self.errors['error_file_name'] = (
                ERROR_MESSAGES['error_file_name']['empty']
            )
            return False
        return True

    def validate_extension(self) -> bool:
        file_extension = os.path.splitext(self.file_name)[1].lower()
        if file_extension not in self.allowed_extensions:
            self.errors['error_extension'] = (
                ERROR_MESSAGES['error_extension']['incorrect_format']
            )
            return False
        return True

    def validate_size(self) -> bool:
        file_size = os.fstat(self.uploaded_file.stream.fileno()).st_size
        if file_size > self.max_size:
            self.errors['error_size'] = (
                    ERROR_MESSAGES['error_size']['incorrect_size'] +
                    (f'Размер Вашего файла {(file_size / 1_048_576):.2f} МБ. '
                     f'Допустимый размер = {int(self.max_size / 1_048_576)} МБ.')
            )
            return False
        return True


@dataclass
class FileNameModifierAndSave:
    user_email: str
    uploaded_file: object
    upload_folder: str

    def __post_init__(self):
        self.save_file()

    def create_name(self) -> str:
        current_time = dt.datetime.now().strftime(
            '%d-%m-%Y_%H-%M-%S'
        )
        file_name = (
            f'{self.user_email}_'
            f'{current_time}_'
            f'{self.uploaded_file.filename}'
        )
        return file_name

    def save_file(self) -> NoReturn:
        file_name = self.create_name()
        file_path = self.upload_folder + file_name
        self.uploaded_file.save(file_path)
