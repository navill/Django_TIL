from django.core.exceptions import ValidationError


def validate_tasty(value):
    if not value.startswith(u"Tasty"):
        msg= u"Must start with Tasty"
        raise ValidationError(msg)