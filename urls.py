from django.conf.urls import url
from django.views.generic import ListView
from django.urls import path, re_path
from .models import Donor
from .views import *

app_name = 'zengshu'

urlpatterns = [
    re_path(r'^$',
            DonorTopView.as_view(),
            name='home_page'),
    re_path(r'^(?P<page>\d+)$',
            DonorListView.as_view(),
            name='list_donors'),
    re_path(r'^donors_list_page$',
            DonorListCheck.as_view(),
            name='list_donors_page'),
    re_path(r'^donor/(?P<pk>\d+)$',
            DonorDetailView.as_view(),
            name='detail_donor'),
    re_path(r'^search$',
            DonorSearchView.as_view(),
            name='search_donor'),
    re_path(r'^book/(?P<pk>\d+)$',
            BookDetailView.as_view(),
            name='detail_book'),
    re_path(r'^donor_index',
            ListView.as_view(
                queryset=Donor.objects.order_by("name_index",
                                                "-donor_type",
                                                "name",
                                                ),
                context_object_name='donors',
                template_name='zengshu/donor_index.html'),
            name='donor_index'),
    re_path(r'^feeds/latest/$',
            LatestDonorFeed(),
            name="feed_latest"),
]
