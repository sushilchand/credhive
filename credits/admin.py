from credits.models import Bank, Company, Loan, Turnover
from django.contrib import admin

# Register your models here.
admin.site.register(Company)
admin.site.register(Loan)
admin.site.register(Turnover)
admin.site.register(Bank)
