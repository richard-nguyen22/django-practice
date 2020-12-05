from django.views.generic import TemplateView

class HomepageView(TemplateView):
  template_name = 'index.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['my_statement'] = 'You\'re the best!'
    return context

  def get_build(self):
    return "You are very good at software engineering. \nYou build" + \
      " software systems that are reliable, functional using TDD and clean code practice"

