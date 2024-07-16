from base_models import db

# from projects.auth.models import User
# db.create_tables([User])

# from projects.auth.models import UserRole
#
# db.create_tables([UserRole])
# UserRole.insert_many([
#     ('None',),
#     ('admin',),
#     ('administration',),
#     ('builders',),
#     ('director',),
#     ('finance',),
#     ('supply',),
# ], fields=[UserRole.name]
# ).execute()
#
# from projects.auth.models import Departments
#
# db.create_tables([Departments])
# Departments.insert_many(
#     [
#         ('Администрация',),
#         ('Бухгалтерия',),
#         ('Логистика',),
#         ('Отдел кадров',),
#         ('ПТО',),
#         ('Руководство',),
#         ('Снабжение',),
#         ('Строительный отдел',),
#         ('Финансовый отдел',),
#         ('Юридический отдел',),
#     ], fields=[
#         Departments.name,
#     ]
# ).execute()

# db.create_tables([TypeDoc, TypeOperation, BankList])
# TypeDoc.insert_many([
#     ('Поступление на р/с',),
#     ('Списание с р/с',),
# ], fields=[
#     TypeDoc.type_doc
# ]
# ).execute()

# TypeOperation.insert_many([
#     ('Оплата от покупателя',),
#     ('Оплата поставщику',),
#     ('Прочее списание',),
# ], fields=[TypeOperation.type_operation]
# ).execute()

# from projects.auth.models import UserAccessCode
# db.create_tables([UserAccessCode])
