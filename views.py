# -*- coding: utf-8 -*-     
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateResponseMixin
from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext as _
from django.urls import reverse, reverse_lazy
from django.db.models import Max, Sum, Count
from django.http import HttpResponseRedirect
import urllib
from datetime import datetime


from .models import Donor, Book
from .utils import DONOR_PAGE_SIZE, DONOR_TOP_SIZE, BOOK_TOP_SIZE
from .form import DonorListPageForm, DonorSearchForm


def set_top_books_and_cover(donor_list):
    for dn in donor_list:
        date = dn.last_donate_date
        dn.top_books = dn.book_set.filter(
            donate_date=date)[:BOOK_TOP_SIZE]
        for bk in dn.top_books:
            cover = bk.get_cover()
            if cover:
                dn.top_cover = cover


class DonorListBase(TemplateResponseMixin):
    template_name = 'zengshu/donor_list.html'

    def get_queryset(self):
        qs = Donor.objects.annotate(
            last_donate_date=Max('book__donate_date'))
        return qs.order_by("-last_donate_date")


class DonorListView(ListView, DonorListBase):
    paginate_by = DONOR_PAGE_SIZE
    context_object_name = 'donors'

    def get_context_data(self, **kwargs):
        context = super(DonorListView, self).get_context_data(**kwargs)
        set_top_books_and_cover(context['donors'])
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
    template_name = 'zengshu/donor_detail.html'

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
        query_raw = urllib.unquote(self.request.META['QUERY_STRING'])
        try:
            if "%u" in query_raw:
                query = query_raw.replace("%u", "\\u").decode("unicode escape")
            else:
                try:
                    query = query_raw.decode('utf-8')
                except UnicodeDecodeError:
                    query = query_raw.decode('GBK')

            query = dict(urllib.parse.parse_qsl(query))
            keyword = query.get('keyword', "")
        except:
            keyword = self.request.REQUEST["keyword"]

        queryset = super(DonorSearchView, self).get_queryset()
        queryset = queryset.filter(name__contains=keyword.strip())

        return queryset

    def render_to_response(self, context, **response_kwargs):
        if ('keyword' in self.request.REQUEST):
            donors = self.get_queryset()
            set_top_books_and_cover(donors)

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


class DonorTopView(ListView, DonorListBase):
    template_name = 'zengshu/donor_top.html'

    def render_to_response(self, context, **response_kwargs):
        queryset = self.get_queryset()
        org_donors = queryset.filter(donor_type=1)[:DONOR_TOP_SIZE]
        personal_donors = queryset.filter(donor_type=0)[:DONOR_TOP_SIZE]
        set_top_books_and_cover(org_donors)
        set_top_books_and_cover(personal_donors)
        context['donor_list_set'] = [org_donors, personal_donors]
        context['indexes'] = Donor.objects.values('name_index').order_by(
            'name_index').annotate(num=Count('name_index'))

        return super(DonorTopView, self).render_to_response(context,
                                                            **response_kwargs)


class BookDetailView(DetailView):
    model = Book
    context_object_name = "book"
    template_name = "zengshu/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['photos'] = self.object.photos.all()
        context['donors'] = self.object.donor.all()

        return context


class LatestDonorFeed(Feed, DonorListBase):
    title = u"最新赠书"
    link = reverse_lazy('home_page')
    description = u"最新赠书人名单"
    item_pubdate = datetime.now()

    def items(self):
        donor_list = self.get_queryset()[:DONOR_TOP_SIZE * 2]
        set_top_books_and_cover(donor_list)
        return donor_list

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        book_list = _("donate:") + _(",").join(
            _("<") + book.name + _(">") for book in item.top_books)

        return book_list

    def item_pubdate(self, item):
        books = item.top_books
        if 0 < len(books):
            date = books[0].donate_date
            return datetime.combine(date, datetime.min.time())
        else:
            return None
