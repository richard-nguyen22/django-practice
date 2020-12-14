import pytest
from ..models import Cheese

# Connect tests with the database
pytestmark = pytest.mark.django_db

def test___str__():
  cheese = Cheese.objects.create(
    name='Test Cheese',
    description='Semi-sweet cheese that is created to test',
    firmness=Cheese.Firmness.SOFT,)
  assert cheese.__str__() == 'Test Cheese'
  assert str(cheese) == 'Test Cheese'
