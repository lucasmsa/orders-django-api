from django.core.validators import RegexValidator
from django.forms import ValidationError
import datetime

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

def validate_deadline(date):
    if date < datetime.date.today():
        raise ValidationError('Date cannot be set to a previous date')