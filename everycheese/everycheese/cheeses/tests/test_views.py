import pytest
from pytest_django.asserts import (
  assertContains, assertRedirects
)
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from everycheese.users.models import User
from ..models import Cheese
from ..views import (
  CheeseCreateView, CheeseListView, CheeseDetailView
)
from .factories import CheeseFactory

pytestmark = pytest.mark.django_db

def test_good_cheese_list_view_expanded(rf):
  # Determine url
  url = reverse('cheeses:list')
  # rf is pytest shortcut for django.test.RequestFactory. Generate a request
  # as if from a user accessing the cheese list view
  request = rf.get(url)
  # call as_view() to make a callable object callable_obj is similar to a FBV
  callable_obj = CheeseListView.as_view()
  # Pass the request into callable_obj to get http response
  response = callable_obj(request)
  # Test http response has 'Cheese List' in the html and has 200 responsecode
  assertContains(response, 'Cheese List')

def test_good_cheese_detail_view(rf):
  # Get a cheese from the CheeseFactory
  cheese = CheeseFactory()
  # Make a request for the new cheese
  url = reverse('cheeses:detail', kwargs={'slug':cheese.slug})
  request = rf.get(url)
  # Use the request to get the response
  callable_obj = CheeseDetailView.as_view()
  response = callable_obj(request, slug=cheese.slug)
  # Test validity of response
  assertContains(response, cheese.name)
  
def test_good_cheese_create_view(rf, admin_user):
  # Order some cheese from the CheeseFactory
  cheese = CheeseFactory()
  # Make a request for our new cheese
  request = rf.get(reverse('cheeses:add'))
  # Add an authenticated user
  request.user = admin_user
  # User request to get the response
  response = CheeseCreateView.as_view()(request)
  # Test request validity
  assert response.status_code == 200
  
def test_cheese_list_contains_2_cheeses(rf):
  '''
  In the contain of the cheese list, test the cheese name can be found 
  '''
  # Create new cheeses
  cheese1 = CheeseFactory()
  cheese2 = CheeseFactory()
  # Get a request & response
  request = rf.get(reverse('cheeses:list'))
  response = CheeseListView.as_view()(request)
  # Assert cheese name in the list
  assertContains(response, cheese1.name)
  assertContains(response, cheese2.name)

def test_detail_contains_cheese_data(rf):
  cheese = CheeseFactory()
  url = reverse('cheeses:detail', kwargs={'slug':cheese.slug})
  request = rf.get(url)
  callable_obj = CheeseDetailView.as_view()
  response = callable_obj(request, slug=cheese.slug)
  assertContains(response, cheese.name)
  assertContains(response, cheese.get_firmness_display())
  assertContains(response, cheese.country_of_origin.name)
  
def test_cheese_create_form_valid(rf, admin_user):
  # Submit the cheese add form
  form_data = {
    'name': 'Paski Sir',
    'description': 'A salty hard cheese',
    'firmness': Cheese.Firmness.HARD
  }
  request = rf.post(reverse('cheeses:add'), form_data)
  request.user = admin_user
  response = CheeseCreateView.as_view()(request)
  cheese = Cheese.objects.get(name='Paski Sir')
  assert cheese.description == 'A salty hard cheese'
  assert cheese.firmness == Cheese.Firmness.HARD
  assert cheese.creator == admin_user