from django.conf.urls import patterns, url
from django.views.generic import ListView
from zenshu.models import Donor
from zenshu.views import *

donors_list_view = DonorListView.as_view()

urlpatterns = patterns('',
                       url(r'^$',
                           donors_list_view,
                           name='home_page'),
                       url(r'^(?P<page>\d+)$',
                           donors_list_view,
                           name='list_donors'),
                       url(r'^donors_list_page$',
                           DonorListCheck.as_view(),
                           name='list_donors_page'),
                       url(r'^detail/(?P<pk>\d+)$',
                           DonorDetailView.as_view(),
                           name='detail_donor'),
                       url(r'^search$',
                           DonorSearchView.as_view(),
                           name='search_donor'),
                       url(r'^book/(?P<pk>\d+)$',
                           BookDetailView.as_view(),
                           name='detail_book'),
                       url(r'^donor_index',
                           ListView.as_view(
                               queryset=Donor.objects.order_by("name_index",
                                                               "-donor_type",
                                                               "name",
                                                               ),
                               context_object_name='donors',
                               template_name='zenshu/donor_index.html'),
                           name='donor_index')
                       )
