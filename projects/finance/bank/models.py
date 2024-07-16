import pandas as pd
from peewee import (
    CharField,
    DecimalField,
    ForeignKeyField
)

from base_models import BaseModel
from settings import EXCEL

data = pd.read_excel(EXCEL)


class TypeDoc(BaseModel):
    type_doc = CharField()


class TypeOperation(BaseModel):
    type_operation = CharField()


class BankList(BaseModel):
    num_pp = DecimalField()
    date_pp = CharField(max_length=10)
    type_doc = ForeignKeyField(TypeDoc)
    sum_doc = DecimalField(decimal_places=2)
    information = CharField()
    contractor = CharField()
    type_operation = ForeignKeyField(TypeOperation)
    comment_doc = CharField()

# print(data.columns)
#
# for index, row in data.iterrows():
#     BankList.create(
#         num_pp=row.iloc[0],
#         date_pp=row.iloc[1],
#         type_doc=row.iloc[2],
#         sum_doc=row.iloc[3],
#         information=row.iloc[4],
#         contractor=row.iloc[5],
#         type_operation=row.iloc[6],
#         comment_doc=row.iloc[7],
#     )
