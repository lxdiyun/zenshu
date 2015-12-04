from django.contrib.admin.filters import FieldListFilter
from django.db.models import Max, Sum
from django.contrib import admin


class DonorAnnotateFilter(FieldListFilter):
    template = 'admin/donor_annotate_filter.html'

    def expected_parameters(self):
        return []

    def choices(self, cl):
        return []

    def queryset(self, request, queryset):
        return queryset.annotate(amount=Sum('book__amount'),
                                 last_donate_date=Max('book__donate_date'))


def custom_titled_filter(title):
    class CustomTitleWrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return CustomTitleWrapper
