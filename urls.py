from django.conf.urls import patterns, url
from zenshu.views import *

donators_list_view = DonatorListView.as_view()

urlpatterns = patterns('',
                       url(r'^$',
                           donators_list_view,
                           name='home_page'),
                       url(r'^(?P<page>\d+)$',
                           donators_list_view,
                           name='list_donators'),
                       url(r'^donators_list_page$',
                           DonatorListCheck.as_view(),
                           name='list_donators_page'),
                       url(r'^detail/(?P<pk>\d+)$',
                           DonatorDetailView.as_view(),
                           name='detail_donator'),
                       url(r'^search/(?P<keyword>.+)$',
                           DonatorSearchView.as_view(),
                           name='search_donator'),
                       )
