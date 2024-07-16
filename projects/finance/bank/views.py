from flask import (
    Blueprint, render_template,
    session, abort,
    request, redirect,
    url_for,
)

from settings import (
    UPLOAD_FOLDER,
    ALLOWED_EXTENSIONS_BANK,
    MAX_SIZE_BANK,
    SESSION_KEY_USER_ID
)

bank_bp = Blueprint(
    'bank',
    __name__,
    url_prefix='/bank'
)


@bank_bp.before_request
def check_session():
    if SESSION_KEY_USER_ID not in session:
        return redirect(url_for('auth.login'))


@bank_bp.get('/')
def bank():
    # data = BankList.select()
    return render_template(
        'personal_cabinet/bank/bank_page.html',
    )


@bank_bp.get('/add_file')
def add_file():
    return render_template(
        'personal_cabinet/bank/add_bank_file_page.html',
        title='Загрузка банка',
        message=session.pop('message', None),
    )


@bank_bp.post('/add_file')
def upload_file():
    uploaded_file = request.files['resume']
    try:
        """Валидация файла по параметрам."""
        check_file = FileValidation(
            uploaded_file,
            ALLOWED_EXTENSIONS_BANK,
            MAX_SIZE_BANK
        )
        valid, errors = check_file.validate()

    except Exception as e:
        message = f'Произошла ошибка: {str(e)}'
        session['message'] = message

        # Todo: добавить запись в логи

    else:
        if valid:
            """Выводим почту из сессии."""
            user_email = session.get('userLogged', 'unknown_user')

            saved_file = FileNameModifierAndSave(
                user_email,
                uploaded_file,
                UPLOAD_FOLDER
            )
            message = 'Успешная загрузка!'
            session['message'] = message

            # Todo: добавить запись в логи
        else:
            return render_template(
                'personal_cabinet/bank/add_bank_file_page.html',
                error_file_name=errors.get('error_file_name', ''),
                error_extension=errors.get('error_extension', ''),
                error_size=errors.get('error_size', ''),
            )

    return redirect(url_for('bank.add_file'))
