from django.conf.urls import patterns, url
from django.views.generic import ListView
from zenshu.models import Donator

list_donators_view = ListView.as_view(
    model=Donator,
    context_object_name='donators',
    paginate_by=8,
    template_name='zenshu/donator_list.html'
)

urlpatterns = patterns('',
                       url(r'^$',
                           list_donators_view,
                           name='home_page'),
                       url(r'^(?P<page>\d+)$',
                           list_donators_view,
                           name='list_donators'),
                       )
