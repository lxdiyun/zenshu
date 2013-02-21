from django.views.generic import ListView
from django.views.generic.edit import FormView
from zenshu.models import Donator
from zenshu.utils import DONATOR_PAGE_SIZE
from zenshu.form import DonatorListPageForm
from django.core.urlresolvers import reverse
from django.db.models import Max
from django.http import HttpResponseRedirect


class DonatorListView(ListView):
    queryset = Donator.objects.annotate(last_donate_date=Max('book__donate_date')).order_by("-last_donate_date")
    context_object_name = 'donators'
    paginate_by = DONATOR_PAGE_SIZE
    template_name = 'zenshu/donator_list.html'

class DonatorListCheck(DonatorListView, FormView):
    form_class = DonatorListPageForm

    def form_valid(self, form):
        page = form.cleaned_data["page"]
        return HttpResponseRedirect(reverse("list_donators", args=[page]))

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse("list_donators", args=[1]))
