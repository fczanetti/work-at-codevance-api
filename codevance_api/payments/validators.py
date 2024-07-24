from datetime import date

from rest_framework.serializers import ValidationError


def date_not_before_today(value):
    """
    Certifies the date informed is not
    before the today.
    """
    if not value >= date.today():
        raise ValidationError("Inform a date greater than or equal today.")
    return value
