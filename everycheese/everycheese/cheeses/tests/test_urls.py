import pytest
from django.urls import reverse, resolve
from .factories import CheeseFactory

pytestmark = pytest.mark.django_db

# Create a fixture for "cheese = CheeseFactory(), so do not need to rewrite the
# code again in every test
@pytest.fixture
def cheese():
  return CheeseFactory()

def test_list_reverse():
  '''
  cheeses:list should reverse to "/cheeses/" url
  '''
  assert reverse('cheeses:list') == '/cheeses/'
  
def test_list_resolve():
  '''
  "/cheeses/" should resolve to cheeses:list
  '''
  assert resolve('/cheeses/').view_name == 'cheeses:list'
  
def test_add_reverse():
  assert reverse('cheeses:add') == '/cheeses/add/'

def test_add_resolve():
  assert resolve('/cheeses/add/').view_name == 'cheeses:add'
  
def test_detail_reverse(cheese):
  """
  cheeses:detail should reverse to /cheeses/cheeseslug/
  """
  url = reverse('cheeses:detail', kwargs={'slug':cheese.slug})
  assert url == f'/cheeses/{cheese.slug}/'
  
def test_detail_resolve(cheese):
  """
  /cheeses/cheeseslug/ should resolve to cheeses:detail
  """
  url = f'/cheeses/{cheese.slug}/'
  assert resolve(url).view_name == 'cheeses:detail'