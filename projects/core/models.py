from peewee import (
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKeyField,
)

from base_models import BaseModel
from projects.auth.models import User


class StatusContract(BaseModel):
    """Статус контракта."""
    type = CharField(max_length=20, unique=True)


class TypeAdditionalAgreement(BaseModel):
    """Тип дополнительного соглашения."""
    name = CharField(max_length=20, unique=True)


class TypeWarrantyRetention(BaseModel):
    """Тип гарантийного удержания."""
    name = CharField(max_length=20, unique=True)


class Employer(BaseModel):
    """Заказчик."""
    name = CharField(max_length=50)
    site = CharField(max_length=100)
    telephone = CharField(max_length=20)
    sum_contracts = DecimalField(null=True)


class ContractModel(BaseModel):
    """Общая модель для контрактов."""

    class Meta:
        order_by = ('status', 'employer',)


class Contract(ContractModel):
    """Основные данные контракта."""
    status = ForeignKeyField(StatusContract)
    employer = ForeignKeyField(Employer)
    object = CharField(max_length=30)
    address = CharField(max_length=100)
    name = CharField(max_length=50, null=True)
    date_contract = DateTimeField(formats='%d.%m.%Y', null=True)
    start_date = DateTimeField(formats='%d.%m.%Y', null=True)
    end_date = DateTimeField(formats='%d.%m.%Y', null=True)
    description = CharField(max_length=100, null=True)
    amount = DecimalField()
    user_manager = ForeignKeyField(User, backref='contracts')
    warranty_retention = ForeignKeyField(TypeWarrantyRetention, null=True)
    additional_agreement = ForeignKeyField(TypeAdditionalAgreement, null=True)


class AdditionalAgreement(ContractModel):
    """Дополнительное соглашение."""
    status = ForeignKeyField(StatusContract)
    employer = ForeignKeyField(Employer)
    name = CharField(max_length=50)
    date_agreement = DateTimeField(formats='%d.%m.%Y', null=True)
    main_contract = ForeignKeyField(Contract)
    type = ForeignKeyField(TypeAdditionalAgreement, null=True)
    description = CharField(max_length=100, null=True)
    amount = DecimalField()
