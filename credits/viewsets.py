import logging

from credits.models import Bank, Company, Loan, Turnover
from credits.serializers import (
    BankSerializer,
    CompanySerializer,
    CreditSerializer,
    LoanSerializer,
    TurnoverSerializer,
)
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

logger = logging.getLogger(__name__)


# Create your views here.
class CompanyViewset(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    http_method_names = ["get", "post", "put"]
    permission_classes = [IsAuthenticated]


class TurnoverViewset(viewsets.ModelViewSet):
    queryset = Turnover.objects.all()
    serializer_class = TurnoverSerializer
    http_method_names = []


class LoanViewset(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    http_method_names = []


class BankViewset(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    http_method_names = []


class CreditViewset(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CreditSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def list(self, request, *args, **kwargs):
        logger.info("List all the credit information of all the companies")
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # dummy response
        logger.info("Dummy API call to create credit information")
        return Response(
            "Credit information was created successfully",
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk, partial=True):
        # dummy response
        logger.info("Dummy API call to update credit information")
        return Response(
            "Credit information for company id {} updated successfully".format(pk),
            status=status.HTTP_200_OK,
        )
