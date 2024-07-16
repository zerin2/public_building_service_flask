import pytest
from projects.auth.models import FormValidation
from projects.auth.config import ERROR_MESSAGES


@pytest.mark.parametrize(
    [
        'user_name', 'user_surname',
        'user_email', 'user_password',
        'user_select_department', 'expected'
    ],
    [
        (
                'Петя',
                'Петров',
                'petya@asf.ru',
                '13245678df',
                'ПТО',
                (True, {}),
        ),
        (
                'СЕРёГА',
                'Ким',
                'dd@asf.ru',
                '13245678dfasd',
                'Руководство',
                (True, {}),
        ),
        (
                'СЕРёГАваd',
                'Ким',
                'dd@asf.ru',
                '13245678dfasd',
                'Руководство',
                (False, {'error_name': ERROR_MESSAGES['error_name']['incorrect_characters']}),

        ),
        (
                'Ким',
                'Ким312',
                'dd@asf.ru',
                '13245678dfasd',
                'Руководство',
                (False, {'error_surname': ERROR_MESSAGES['error_surname']['incorrect_characters']}),

        ),
        (
                'Ким',
                'Кимfcsa',
                'dd@asf.ru',
                '13245678dfasd',
                'Руководство',
                (False, {'error_surname': ERROR_MESSAGES['error_surname']['incorrect_characters']}),

        ),
        (
                'Ким',
                'Ким',
                'dd@asf.rываыфu',
                '13245678dfasd',
                'Руководство',
                (False, {'error_email': ERROR_MESSAGES['error_email']['incorrect_format']}),

        ),
        (
                'Ким',
                'Ким',
                'ddasf.ru',
                '13245678dfasd',
                'Руководство',
                (False, {'error_email': ERROR_MESSAGES['error_email']['incorrect_format']}),

        ),
        (
                'Ким',
                'Ким',
                'dda@sf.ru',
                '',
                'Руководство',
                (False, {'error_password': ERROR_MESSAGES['error_password']['empty']}),

        ),
        (
                'Ким',
                'Ким',
                'dda@sf.ru',
                '3213',
                'Руководство',
                (False, {'error_password': ERROR_MESSAGES['error_password']['incorrect_length']}),

        ),
        (
                'Ким',
                'Ким',
                'dda@sf.ru',
                '321ывамвы3',
                'Руководство',
                (False, {'error_password': ERROR_MESSAGES['error_password']['incorrect_characters']}),

        ),
        (
                'Ким',
                'Ким',
                'dda@sf.ru',
                '321523532523215325',
                'Руководство',
                (False, {'error_password': ERROR_MESSAGES['error_password']['incorrect_format']}),

        ),
        (
                'Ким',
                'Ким',
                'dda@sf.ru',
                '32152353252qwad3215325',
                '',
                (False, {'error_department': ERROR_MESSAGES['error_department']['empty']}),

        ),
        (
                'Кимddd',
                'Ким',
                'ddasf.ru',
                '3215235323215325',
                'Руководство',
                (False, {
                    'error_name': ERROR_MESSAGES['error_name']['incorrect_characters'],
                    'error_password': ERROR_MESSAGES['error_password']['incorrect_format'],
                    'error_email': ERROR_MESSAGES['error_email']['incorrect_format'],
                }),

        ),
        (
                'Ким232',
                'Кимdd',
                'ddasf.ru',
                '3215235323215325',
                '',
                (False, {
                    'error_name': ERROR_MESSAGES['error_name']['incorrect_characters'],
                    'error_email': ERROR_MESSAGES['error_email']['incorrect_format'],
                    'error_surname': ERROR_MESSAGES['error_surname']['incorrect_characters'],
                    'error_password': ERROR_MESSAGES['error_password']['incorrect_format'],
                    'error_department': ERROR_MESSAGES['error_department']['empty'],
                }),

        ),
        (
                'Ким232',
                'Кимdd',
                'ddasf.ru',
                '3215235323215325',
                'ПТ',
                (False, {
                    'error_name': ERROR_MESSAGES['error_name']['incorrect_characters'],
                    'error_email': ERROR_MESSAGES['error_email']['incorrect_format'],
                    'error_surname': ERROR_MESSAGES['error_surname']['incorrect_characters'],
                    'error_password': ERROR_MESSAGES['error_password']['incorrect_format'],
                    'error_department': ERROR_MESSAGES['error_department']['empty'],
                }),

        ),
        (
                '123214',
                'Ким',
                'test@test.ru',
                'аыаыфа',
                'ПТО',
                (False, {
                    'error_name': ERROR_MESSAGES['error_name']['incorrect_characters'],
                    'error_email': ERROR_MESSAGES['error_email']['existing_user'],
                    'error_password': ERROR_MESSAGES['error_password']['incorrect_length'],
                }),
        ),
    ]
)
def test_form_validation(
        user_name, user_surname, user_email,
        user_password, user_select_department, expected
):
    assert FormValidation(
        user_name,
        user_surname,
        user_email,
        user_password,
        user_select_department,
    ).validate() == expected
