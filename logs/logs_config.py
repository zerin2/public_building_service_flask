from loguru import logger


admin_logger = logger
admin_logger.add('logs/admin/info.log', rotation='10 MB', level='INFO')
admin_logger.add('logs/admin/error.log', rotation='10 MB', level='ERROR')

auth_logger = logger
auth_logger.add('logs/auth/info.log', rotation='10 MB', level='INFO')
auth_logger.add('logs/auth/error.log', rotation='10 MB', level='ERROR')

core_logger = logger
core_logger.add('logs/core/info.log', rotation='10 MB', level='INFO')
core_logger.add('logs/core/error.log', rotation='10 MB', level='ERROR')

db_logger = logger
db_logger.add('logs/db/info.log', rotation='10 MB', level='INFO')
db_logger.add('logs/db/error.log', rotation='10 MB', level='ERROR')

finance_logger = logger
finance_logger.add('logs/finance/info.log', rotation='10 MB', level='INFO')
finance_logger.add('logs/finance/error.log', rotation='10 MB', level='ERROR')

has_logger = logger
has_logger.add('logs/help_and_support/info.log', rotation='10 MB', level='INFO')
has_logger.add('logs/help_and_support/error.log', rotation='10 MB', level='ERROR')
