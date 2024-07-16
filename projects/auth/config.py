"""Специальные знаки и символы для проверки."""
SPECIAL_CHARACTERS = '!#$%&()*+,-./:;<=>?@[]^_{|}~'
LOWERCASE_CYRILLIC = ''.join(chr(i) for i in range(0x0430, 0x0450)) + 'ё' + 'Ё'
UPPERCASE_CYRILLIC = ''.join(chr(i) for i in range(0x0410, 0x0430))
CYRILLIC = LOWERCASE_CYRILLIC + UPPERCASE_CYRILLIC

"""Сообщения об ошибках, используемые при валидации данных."""
ERROR_MESSAGES = {
    'error_login': {
        'general': 'Неверный логин или пароль. Попробуйте снова.',
    },
    'error_email': {
        'empty': 'Не указан email.',
        'incorrect_length': 'Не корректный email. Проверьте количество символов.',
        'incorrect_format': 'Не корректный формат email.',
        'no_find': 'Пользователь с таким email не существует.'
    },
    'error_name': {
        'empty': 'Не указано имя пользователя.',
        'incorrect_length': 'Некорректное имя. Проверьте количество символов.',
        'incorrect_characters': 'Некорректное имя. Используйте кириллицу.',
        'incorrect_characters_spec': 'Не корректное имя. Не используйте специальные символы.',
    },
    'error_surname': {
        'empty': 'Не указана фамилия пользователя.',
        'incorrect_length': 'Некорректная фамилия. Проверьте количество символов.',
        'incorrect_characters': 'Некорректная фамилия. Используйте кириллицу.',
        'incorrect_characters_spec': 'Не корректная фамилия. Не используйте специальные символы.',
    },
    'error_password': {
        'empty': 'Не указан пароль. Пароль должен содержать не менее 8 символов. Используйте латиницу и цифры.',
        'incorrect_length': 'Некорректная длинна. Пароль должен содержать не менее 8 символов.'
                            ' Используйте латиницу и цифры.',
        'incorrect_characters': 'Не используйте кириллицу. Пароль должен содержать не менее 8 символов.'
                                ' Используйте латиницу и цифры.',
        'incorrect_format': 'Некорректный формат. Пароль должен содержать не менее 8 символов.'
                            ' Используйте латиницу и цифры.',
    },
    'error_password_repeat': {
        'mismatch': 'Пароли не совпадают.',
    },
    'error_access_code': {
        'incorrect_code': 'Неверный код доступа.',
    },
    'error_department_id': {
        'empty': 'Не указали департамент.',
        'incorrect': 'Указан неверный департамент.',
    },
    'error_extension': {
        'incorrect_format': 'Недопустимое расширение файла.',
    },
    'error_size': {
        'incorrect_size': 'Превышение размера файла. ',
    },
    'error_file_name': {
        'empty': 'Пустое название файла.',
    },
}
