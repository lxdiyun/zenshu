from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateResponseMixin
from zenshu.models import Donator, Book
from zenshu.utils import DONATOR_PAGE_SIZE
from zenshu.form import DonatorListPageForm, DonatorSearchForm
from django.core.urlresolvers import reverse
from django.db.models import Max, Sum
from django.http import HttpResponseRedirect
from django.utils.encoding import smart_str


class DonatorListBase(TemplateResponseMixin):
    template_name = 'zenshu/donator_list.html'

    def get_queryset(self):
        qs = Donator.objects.annotate(
            last_donate_date=Max('book__donate_date'))
        return qs.order_by("-last_donate_date")


class DonatorListView(ListView, DonatorListBase):
    paginate_by = DONATOR_PAGE_SIZE
    context_object_name = 'donators'


class DonatorListCheck(FormView):
    form_class = DonatorListPageForm

    def form_valid(self, form):
        page = form.cleaned_data["page"]
        return HttpResponseRedirect(reverse("list_donators", args=[page]))

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse("list_donators", args=[1]))


class DonatorDetailView(DetailView):
    model = Donator
    context_object_name = 'donator'
    template_name = 'zenshu/donator_detail.html'

    def get_queryset(self):
        queryset = super(DonatorDetailView, self).get_queryset()
        queryset = queryset.annotate(last_donate_date=Max('book__donate_date'),
                                     total_donate=Sum('book__amount'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(DonatorDetailView, self).get_context_data(**kwargs)
        context['books'] = Book.objects.filter(donator=self.object)

        return context


class DonatorSearchView(FormView, DonatorListBase):
    form_class = DonatorSearchForm

    def get_queryset(self):
        keyword = self.request.REQUEST.get('keyword', "")
        print(smart_str(keyword))
        queryset = super(DonatorSearchView, self).get_queryset()
        queryset = queryset.filter(name__contains=keyword)

        return queryset

    def render_to_response(self, context, **response_kwargs):
        if ('keyword' in self.request.REQUEST):
            donators = self.get_queryset()
            print donators

            if (donators and (donators.count() == 1)):
                return HttpResponseRedirect(donators[0].get_absolute_url())
            else:
                context['donators'] = donators
                return super(DonatorSearchView,
                             self).render_to_response(context,
                                                      **response_kwargs)
        else:
            return HttpResponseRedirect(reverse("list_donators", args=[1]))

    def form_valid(self, form):
        nextUrl = reverse('search_donator')
        nextUrl += "?keyword=%s" % form.cleaned_data['keyword']

        return HttpResponseRedirect(nextUrl)

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse("list_donators", args=[1]))
