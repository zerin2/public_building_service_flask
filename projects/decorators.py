from flask import (
    abort,
    redirect,
    request,
    url_for,
    session,
)
from functools import wraps

from flask_wtf.csrf import CSRFError, validate_csrf

from settings import SESSION_KEY_USER_ID


def csrf_valid(f):
    """Автоматическая проверка токена из шаблона."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            validate_csrf(
                request.form.get('csrf_token')
            )
        except CSRFError:
            abort(400)
        return f(*args, **kwargs)

    return decorated_function


def login_required(f):
    """Проверка сессии."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if SESSION_KEY_USER_ID not in session:
            return redirect(
                url_for('auth.login')
            )
        return f(*args, **kwargs)

    return decorated_function
