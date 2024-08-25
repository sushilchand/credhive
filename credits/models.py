import datetime
import uuid

from credhive.models import TimestampModel
from credits.types import LOAN_STATUS
from django.db import models


# Create your models here.
class Company(TimestampModel):
    name = models.CharField(max_length=40, unique=True)
    readable_id = models.CharField(max_length=50, unique=True, blank=True)
    address = models.TextField(max_length=100)
    regitration_date = models.DateField()
    employee_count = models.SmallIntegerField()
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=30)
    website = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Companies"

    def generate_readable_id(self):
        # U82990DL2023PTC423896
        # UXXXXXXYYZZZZPTCWWWWWW (example format explanation)
        prefix = "U"
        cin_code = "82990"  # Example CIN code (you can make this dynamic if needed)
        state_code = "DL"  # State code (e.g., 'DL' for Delhi)
        year = datetime.datetime.now().year
        ptc_code = "PTC"
        # Unique sequence number for the company, for simplicity using uuid here, but it can be any other mechanism
        unique_id = str(uuid.uuid4().int)[:6]  # Take first 6 digits from uuid

        # Construct the readable_id
        self.readable_id = f"{prefix}{cin_code}{state_code}{year}{ptc_code}{unique_id}"

    def save(self, *args, **kwargs):
        if not self.readable_id:
            self.generate_readable_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}-{}".format(self.readable_id, self.name)


class Turnover(TimestampModel):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    total = models.FloatField(default=0.0)
    profit = models.FloatField(default=0.0)
    fiscal_year = models.SmallIntegerField()
    report_date = models.DateField()

    class Meta:
        verbose_name_plural = "Turnovers"

    def __str__(self):
        return "{}-{}".format(self.company.name, self.fiscal_year)


class Bank(TimestampModel):
    name = models.CharField(max_length=40, unique=True)
    address = models.TextField(max_length=100)

    class Meta:
        verbose_name_plural = "Banks"

    def __str__(self):
        return self.name


class Loan(TimestampModel):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    date = models.DateField()
    provider = models.ForeignKey(Bank, on_delete=models.DO_NOTHING)
    status = models.SmallIntegerField(LOAN_STATUS.choices())

    class Meta:
        verbose_name_plural = "Loans"

    def __str__(self):
        return "{}-{}".format(self.company.name, self.status)
