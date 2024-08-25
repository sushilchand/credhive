import logging
import random

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate dummy data for all models"

    def handle(self, *args, **kwargs):
        fake = Faker()
        app_config = apps.get_app_config("credits")
        models = app_config.get_models()

        with transaction.atomic():
            for model in models:
                logger.info("Generating data for model {}".format(model))
                for _ in range(50):  # Number of records to generate per model
                    obj = model()

                    for field in model._meta.fields:
                        if field.name == "id" or field.name == "readable_id":
                            continue

                        if field.name == "email":
                            setattr(obj, field.name, fake.email())
                        elif field.name == "fiscal_year":
                            setattr(
                                obj, field.name, fake.random_int(min=1980, max=2024)
                            )
                        elif field.name == "website":
                            setattr(obj, field.name, fake.url())
                        elif field.name == "employee_count":
                            setattr(obj, field.name, fake.random_int(min=1, max=200))
                        elif field.name == "status":
                            setattr(obj, field.name, fake.random_int(min=1, max=3))
                        elif field.name == "contact":
                            setattr(obj, field.name, fake.phone_number())
                        elif field.get_internal_type() == "CharField":
                            setattr(
                                obj,
                                field.name,
                                fake.text(max_nb_chars=field.max_length),
                            )
                        elif field.get_internal_type() == "TextField":
                            setattr(obj, field.name, fake.text())
                        elif field.get_internal_type() == "IntegerField":
                            setattr(obj, field.name, random.randint(1, 100))
                        elif field.get_internal_type() == "FloatField":
                            setattr(obj, field.name, random.uniform(1.0, 100.0))
                        elif field.get_internal_type() == "DateField":
                            setattr(obj, field.name, fake.date())
                        elif field.get_internal_type() == "DateTimeField":
                            setattr(obj, field.name, fake.date_time())
                        elif field.get_internal_type() == "BooleanField":
                            setattr(obj, field.name, random.choice([True, False]))
                        elif field.get_internal_type() == "ForeignKey":
                            related_model = field.related_model
                            related_obj = related_model.objects.order_by("?").first()
                            if related_obj:
                                setattr(obj, field.name, related_obj)
                        # Add other field types as needed
                    obj.save()

        self.stdout.write(
            self.style.SUCCESS("Successfully generated dummy data for all models")
        )
