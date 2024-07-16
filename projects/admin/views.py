from flask import Blueprint, render_template, session, abort

admin_bp = Blueprint(
    'admin',
    __name__,
    url_prefix='/admin'
)


@admin_bp.before_request
def check_session():
    if 'userLogged' not in session:
        abort(401)


# @admin_bp.get('/')
# def admin():
#     return render_template('')
