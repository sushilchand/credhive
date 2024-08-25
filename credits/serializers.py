import datetime
import logging

from credhive.serializers import BaseSerializer
from credits.models import Bank, Company, Loan, Turnover
from credits.schemas import CompanySchema
from credits.types import LOAN_STATUS
from django.db.models import Sum
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


class CompanySerializer(BaseSerializer):
    name = serializers.CharField()
    readable_id = serializers.CharField(read_only=True)
    address = serializers.CharField()
    regitration_date = serializers.DateField()
    employee_count = serializers.IntegerField()
    email = serializers.EmailField()
    contact = serializers.CharField()
    website = serializers.CharField()

    class Meta:
        model = Company
        fields = "__all__"

    def validate(self, data):
        logger.info("Validate company schema for data {}".format(data))
        try:
            validated_data = CompanySchema(**data).dict()
        except ValueError as error:
            # Fetch only the msg field, complete errors list looks like this
            # [
            #   {   "loc": ["contact"],
            #       "msg": "Contact must be exactly 10 digits long.",
            #       "type": "value_error"
            #   }
            # ]
            raise ValidationError(error.errors()[0]["msg"])
        return super().validate(validated_data)


class TurnoverSerializer(BaseSerializer):
    company = CompanySerializer()
    total = serializers.IntegerField()
    profit = serializers.DecimalField(max_digits=9, decimal_places=2)
    fiscal_year = serializers.IntegerField()
    report_date = serializers.DateField()

    class Meta:
        model = Turnover
        fields = "__all__"


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = "__all__"


class LoanSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    company = CompanySerializer()
    amount = serializers.DecimalField(max_digits=9, decimal_places=2)
    date = serializers.DateField()
    provider = BankSerializer()
    status = serializers.IntegerField()

    class Meta:
        model = Loan
        fields = "__all__"


class CreditSerializer(serializers.Serializer):
    credit = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    def get_credit(self, company_obj):
        """A serializer field to calculate the credit information of each company during runtime

        Args:
            company_obj (company model obj): Company object model

        Returns:
            float: The overall credit information for a company
        """
        logger.info("Get credit information for company id : {}".format(company_obj))
        due_loans_amount = Loan.objects.filter(
            company=company_obj, status=LOAN_STATUS.DUE
        ).aggregate(Sum("amount"))["amount__sum"]
        due_loans_amount = due_loans_amount if due_loans_amount else 0.0
        current_year = datetime.date.today().year
        last_two_year_turnover = Turnover.objects.filter(
            company=company_obj, fiscal_year__range=[current_year - 2, current_year]
        ).aggregate(Sum("total"))["total__sum"]
        last_two_year_turnover = (
            last_two_year_turnover if last_two_year_turnover else 0.0
        )
        return round(last_two_year_turnover - due_loans_amount, 2)

    def get_company(self, company_obj):
        return CompanySerializer(company_obj).data

    class Meta:
        model = Company
        fields = ("credit, company",)
