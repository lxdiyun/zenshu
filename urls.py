from django.conf.urls import patterns, url
from django.views.generic import TemplateView
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
                       url(r'base',
                           TemplateView.as_view(
                               template_name='zenshu/base.html'),
                           name='base')
                       )
