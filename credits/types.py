from enum import IntEnum

from django.db import models


class LOAN_STATUS(IntEnum):
    PAID = 1
    DUE = 2
    INITIATED = 3

    @classmethod
    def choices(cls):
        return [(i.name.title(), i.value) for i in cls]
