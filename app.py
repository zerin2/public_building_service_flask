from flask import Flask

from flask_wtf import CSRFProtect

from projects.admin.views import admin_bp
from projects.auth.views import auth_bp
from projects.core.views import (
    core_bp,
    http_forbidden,
    internal_server_error,
    invalid_data,
    page_not_found,
    unauthorized_data,
)
from projects.finance.bank.views import bank_bp

from settings import (
    APP_SECRET_KEY,
    MAX_FILE_UPLOAD_SIZE,
    SESSION_LIFETIME,
)

app = Flask(__name__, static_url_path='/static')

app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_UPLOAD_SIZE
app.permanent_session_lifetime = SESSION_LIFETIME
app.secret_key = APP_SECRET_KEY

csrf = CSRFProtect(app)

app.register_blueprint(admin_bp)
app.register_blueprint(core_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(bank_bp)

app.register_error_handler(400, invalid_data)
app.register_error_handler(401, unauthorized_data)
app.register_error_handler(403, http_forbidden)
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)

if __name__ == '__main__':
    app.run(debug=True)
