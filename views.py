from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateResponseMixin
from zenshu.models import Donor, Book
from zenshu.utils import DONATOR_PAGE_SIZE
from zenshu.form import DonorListPageForm, DonorSearchForm
from django.core.urlresolvers import reverse
from django.db.models import Max, Sum
from django.http import HttpResponseRedirect
from django.utils.encoding import smart_str


class DonorListBase(TemplateResponseMixin):
    template_name = 'zenshu/donor_list.html'

    def get_queryset(self):
        qs = Donor.objects.annotate(
            last_donate_date=Max('book__donate_date'))
        return qs.order_by("-last_donate_date")


class DonorListView(ListView, DonorListBase):
    paginate_by = DONATOR_PAGE_SIZE
    context_object_name = 'donors'

    def get_context_data(self, **kwargs):
        context = super(DonorListView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context


class DonorListCheck(FormView):
    form_class = DonorListPageForm

    def form_valid(self, form):
        page = form.cleaned_data["page"]
        return HttpResponseRedirect(reverse("list_donors", args=[page]))

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse("list_donors", args=[1]))


class DonorDetailView(DetailView):
    model = Donor
    context_object_name = 'donor'
    template_name = 'zenshu/donor_detail.html'

    def get_queryset(self):
        queryset = super(DonorDetailView, self).get_queryset()
        queryset = queryset.annotate(last_donate_date=Max('book__donate_date'),
                                     total_donate=Sum('book__amount'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(DonorDetailView, self).get_context_data(**kwargs)
        context['books'] = self.object.book_set.all()

        return context


class DonorSearchView(FormView, DonorListBase):
    form_class = DonorSearchForm

    def get_queryset(self):
        keyword = self.request.REQUEST.get('keyword', "")
        queryset = super(DonorSearchView, self).get_queryset()
        queryset = queryset.filter(name__contains=keyword.strip())

        return queryset

    def render_to_response(self, context, **response_kwargs):
        if ('keyword' in self.request.REQUEST):
            donors = self.get_queryset()

            if (donors and (donors.count() == 1)):
                return HttpResponseRedirect(donors[0].get_absolute_url())
            else:
                context['donors'] = donors
                return super(DonorSearchView,
                             self).render_to_response(context,
                                                      **response_kwargs)
        else:
            return HttpResponseRedirect(reverse("list_donors", args=[1]))

    def form_valid(self, form):
        nextUrl = reverse('search_donor')
        nextUrl += "?keyword=%s" % form.cleaned_data['keyword']

        return HttpResponseRedirect(nextUrl)

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse("list_donors", args=[1]))


class BookDetailView(DetailView):
    model = Book
    context_object_name = "book"
    template_name = "zenshu/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['photos'] = self.object.photos.all()
        context['donors'] = self.object.donor.all()

        return context
