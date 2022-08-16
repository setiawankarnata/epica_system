from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Digunakan untuk memvalidasi fields yang ada di models.py

def empty_value(value):
    if value is None or value == "":
        raise ValidationError(_("Name tidak boleh dikosongkan."), code="Invalid_name")
