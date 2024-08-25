from credits.viewsets import (
    BankViewset,
    CompanyViewset,
    CreditViewset,
    LoanViewset,
    TurnoverViewset,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("company", CompanyViewset, basename="company")
router.register("turnover", TurnoverViewset, basename="turnover")
router.register("loan", LoanViewset, basename="loan")
router.register("bank", BankViewset, basename="bank")
router.register("credit", CreditViewset, basename="credit")
