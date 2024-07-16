from flask import (
    Blueprint, session, render_template,
    redirect, request, url_for,
)

from flask_wtf.csrf import CSRFError, generate_csrf, validate_csrf
from werkzeug.security import generate_password_hash, check_password_hash

from projects.auth.config import ERROR_MESSAGES
from projects.auth.models import User, Departments, UserRole
from projects.auth.validators import (
    PasswordRecovery,
    ValidationForm,
    UserAuth,
)
from projects.decorators import csrf_valid
from logs.logs_config import auth_logger
from settings import (
    SESSION_PERMANENT_VALUE,
    SESSION_KEY_USER_ID,
    SESSION_KEY_ROLE_NAME
)

auth_bp = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)


@auth_bp.before_request
def before_request():
    if SESSION_KEY_USER_ID in session:
        return redirect(
            url_for(
                'core.index',
                user_id=session[SESSION_KEY_USER_ID]
            )
        )

@auth_bp.get('/login')
def login():
    return render_template(
        'auth/login.html',
        csrf_token=generate_csrf(),
        title='Авторизация',
    )


@auth_bp.post('/login')
@csrf_valid
def login_in():
    error = None
    user = None
    try:
        user = UserAuth(
            email=request.form['email'],
            password=request.form['password']
        ).authenticate_user()
    except Exception as e:
        auth_logger.error(
            f'Ошибка при входе: {e}.'
        )
    if user:
        session[SESSION_KEY_USER_ID] = user.id
        session[SESSION_KEY_ROLE_NAME] = user.role.name
        session.permanent = SESSION_PERMANENT_VALUE
        return redirect(url_for('core.index'))
    else:
        error = ERROR_MESSAGES['error_login']['general']
    return render_template(
        'auth/login.html',
        csrf_token=generate_csrf(),
        error=error,
        title='Авторизация',
    )


@auth_bp.get('/registrate')
def registrate():
    if SESSION_KEY_USER_ID in session:
        return redirect(
            url_for('core.index', )
        )
    return render_template(
        'auth/register.html',
        csrf_token=generate_csrf(),
        departments=Departments.select(),
        title='Регистрация на сайте',
    )


@auth_bp.post('/registrate')
@csrf_valid
def input_personal_data():
    form_data = {field: request.form[field] for field in [
        'name',
        'surname',
        'email',
        'password',
        'password_repeat',
        'department_id',
        'access_code'
    ]}
    form = UserAuth(**form_data)
    valid, errors = form.validate()
    if not valid:
        return render_template(
            'auth/register.html',
            csrf_token=generate_csrf(),
            departments=Departments.select(),
            error_email=errors.get('error_email', ''),
            error_name=errors.get('error_name', ''),
            error_surname=errors.get('error_surname', ''),
            error_password=errors.get('error_password', ''),
            error_password_repeat=errors.get('error_password_repeat', ''),
            error_department_id=errors.get('error_department_id', ''),
            error_access_code=errors.get('error_access_code', ''),
        )
    else:
        form.save_user()
        return redirect(url_for('auth.registrate_success'))


@auth_bp.get('/registrate_success')
def registrate_success():
    return render_template(
        'auth/registrate_success.html',
        title='Успешная регистрация',
    )


@auth_bp.get('/password_recovery')
def password_recovery():
    return render_template(
        'auth/forgot-password.html',
        csrf_token=generate_csrf(),
        title='Восстановление пароля',
    )


@auth_bp.post('/password_recovery')
@csrf_valid
def run_password_recovery():
    ##TODO: валидация готова, настроить само восстановление

    try:
        form = PasswordRecovery(email=request.form.get('email'))
    except Exception as e:
        auth_logger.error(
            f'Ошибка восстановления доступа к аккаунту {form.email}.'
        )
    else:
        valid, errors = form.validate_recovery_email()
    if valid:
        return redirect(url_for('auth.recovery_success'))
    else:
        return render_template(
            'auth/forgot-password.html',
            csrf_token=generate_csrf(),
            title='Ошибка восстановления пароля',
            error_email=errors.get('error_email', ''),
        )


@auth_bp.get('/recovery_success')
def recovery_success():
    return render_template(
        'auth/recover_success.html',
        title='Успешное восстановление пароля',
    )
