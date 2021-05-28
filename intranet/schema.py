from ninja.orm import create_schema
from .models import Person

PersonOut = create_schema(
    Person,
    fields=['name', 'email', 'id_number', 'is_staff', 'is_superuser']
)
