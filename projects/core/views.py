from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
)

from .config import ERROR_TEMPLATE, ERROR_LIST
from settings import SESSION_KEY_USER_ID

core_bp = Blueprint(
    'core',
    __name__,
    url_prefix='/'
)


@core_bp.before_request
def before_request():
    """Проверка USER_ID в сессии."""
    if SESSION_KEY_USER_ID not in session:
        return redirect(url_for('auth.login'))


@core_bp.get('/')
def index():
    return render_template(
        'base_index.html',
        title='BAZIS'
    )


@core_bp.errorhandler(400)
def invalid_data(error):
    """
    '400': 'Сервер не может обработать запрос из-за недопустимых данных.'
    """
    return render_template(
        ERROR_TEMPLATE,
        context=ERROR_LIST['400'],
        error=400,
    ), 400


@core_bp.errorhandler(401)
def unauthorized_data(error):
    """
    '401': 'Отказ в доступе. Выполните аутентификация пользователя.'
    """
    return render_template(
        ERROR_TEMPLATE,
        context=ERROR_LIST['401'],
        error=401,
    ), 401


@core_bp.errorhandler(403)
def http_forbidden(error):
    """
    '403': 'Доступ к запрошенному ресурсу запрещен.'
    """
    return render_template(
        ERROR_TEMPLATE,
        context=ERROR_LIST['403'],
        error=403,
    ), 403


@core_bp.errorhandler(404)
def page_not_found(error):
    """
    '404': 'Страница не найдена.'
    """
    return render_template(
        ERROR_TEMPLATE,
        context=ERROR_LIST['404'],
        error=404,
    ), 404


@core_bp.errorhandler(500)
def internal_server_error(error):
    """
    '500': 'Внутренняя ошибка сервера.'
    """
    return render_template(
        ERROR_TEMPLATE,
        context=ERROR_LIST['500'],
        error=500,
    ), 500
