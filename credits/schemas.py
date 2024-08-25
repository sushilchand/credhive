import logging

from credits.models import Bank, Company, Loan
from credits.types import LOAN_STATUS
from djantic import ModelSchema
from pydantic import validator

logger = logging.getLogger(__name__)


class CompanySchema(ModelSchema):
    contact: str

    class Config:
        model = Company
        exclude = [
            "id",
            "created_at",
            "modified_at",
            "readable_id",
        ]

    @validator("contact", allow_reuse=True)
    def validate_contact(cls, value):
        logger.info("Validate contact against schema for value {}".format(value))
        if len(value) != 10:
            raise ValueError("Contact must be exactly 10 digits long.")
        return value


class LoanSchema(ModelSchema):
    status: LOAN_STATUS

    class Config:
        model = Loan

    @classmethod
    def from_django(cls, obj):
        return cls(status=LOAN_STATUS(obj.status))

# Currently we don't support Turnover data to be created/updated from APIs, this can be reused in future once we require that
# class TurnoverSchema(ModelSchema):
#     fiscal_year: int

#     class Config:
#         model = Turnover

#     @validator('fiscal_year', allow_reuse=True)
#     def validate_fiscal_year(cls, value):
#         current_year = datetime.date.today().year
#         if value >= current_year:
#             raise ValueError('Year can only be of past')
#         return value


class BankSchema(ModelSchema):
    class Config:
        model = Bank
