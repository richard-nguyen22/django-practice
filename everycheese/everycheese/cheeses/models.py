from django.conf import settings
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField

from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel

class Cheese(TimeStampedModel):
  name = models.CharField('Name of Cheese', max_length=255)
  # Use AutoSlugField to populate from "name" field
  slug = AutoSlugField('Cheese Address', unique=True, always_update=False,
    populate_from='name')
  # TextField's length can exceed 255, CharField cannot
  description = models.TextField('Description', blank=True)
  country_of_origin = CountryField("Country of Origin", blank=True)
  creator = models.ForeignKey(settings.AUTH_USER_MODEL,
    null=True, on_delete=models.SET_NULL) # Save user who changes cheese

  def get_absolute_url(self):
    ''' Return absolute URL to the Cheese Detail page'''
    return reverse('cheeses:detail', kwargs={"slug":self.slug})

  def __str__(self):
    return self.name


  class Firmness(models.TextChoices):
    '''
    To do comparision such as:
      if cheese.firmness == Cheese.Firmness.SOFT:
    '''
    UNSPECIFIED = 'unspecified', 'Unspecified'
    SOFT = 'soft', 'Soft'
    SEMI_SOFT = 'semi-soft', 'Semi-Soft'
    SEMI_HARD = 'semi-hard', 'Semi-Hard'
    HARD = 'hard', 'Hard'

  firmness = models.CharField('Firmness', max_length=20,
    choices=Firmness.choices, default=Firmness.UNSPECIFIED)

