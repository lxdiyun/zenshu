from django.contrib.admin.filters import FieldListFilter
from django.db.models import Max, Sum


class DonatorAnnotateFilter(FieldListFilter):
    template = 'zenshu/donator_annotate_filter.html'

    def expected_parameters(self):
        return []

    def choices(self, cl):
        return []

    def queryset(self, request, queryset):
        return queryset.annotate(amount=Sum('book__amount'),
                                 last_donate_date=Max('book__donate_date'))
