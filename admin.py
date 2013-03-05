from zenshu.models import Book, Donator
from zenshu.actions import merge_selected_donators, export_csv_action
from django.contrib import admin
from django.db.models import Max, Sum
from django.utils.translation import ugettext_lazy as _
from daterange_filter.filter import DateRangeFilter


class BookInline(admin.TabularInline):
    model = Book.donator.through
    readonly_fields = ["book_name", "book_donate_date", "book_amount"]
    ordering = ["-book__donate_date"]
    exclude = ['book']
    max_num = 0
    verbose_name = _("book")
    verbose_name_plural = _("book")

    def book_name(self, object):
        return object.book.name
    book_name.short_description = _("book name")
    book_name.admin_order_field = "book__name"

    def book_donate_date(self, object):
        return object.book.donate_date
    book_donate_date.short_description = _("donate date")

    def book_amount(self, object):
        return object.book.amount
    book_amount.short_description = _("amount")


class DonatorAdmin(admin.ModelAdmin):
    list_display = ["name",
                    "last_donate_date",
                    "amount",
                    "description",
                    "contact_info"]
    search_fields = ['name', "description"]
    list_filter = (('book__donate_date', DateRangeFilter),)
    inlines = [BookInline]
    actions = [merge_selected_donators,
               export_csv_action(fields=[
                   ('name', _('donator name')),
                   ('contact_info', _('contact info'))
               ])]

    def get_ordering(self, request):
        return ["-last_donate_date"]

    def queryset(self, request):
        qs = super(DonatorAdmin, self).queryset(request)
        return qs.annotate(last_donate_date=Max('book__donate_date'),
                           amount=Sum('book__amount'))

    def last_donate_date(self, obj):
        return obj.last_donate_date
    last_donate_date.admin_order_field = 'last_donate_date'
    last_donate_date.short_description = _('last donate date')

    def amount(self, obj):
        return obj.amount
    amount.admin_order_field = 'amount'
    amount.short_description = _('amount')

    def lookup_allowed(self, lookup, value):
        print(lookup)
        if lookup in ('book__donate_date__lte', 'book__donate_date__gte'):
            return True
        return super(DonatorAdmin, self).lookup_allowed(lookup, value)


class BookAdmin(admin.ModelAdmin):
    list_display = ["name",
                    "author_name",
                    "amount",
                    "donate_date",
                    "get_donators"]
    search_fields = ['name', "author_name", "donator__name", "donate_date"]
    filter_horizontal = ['donator']
    list_filter = (('donate_date', DateRangeFilter),)

    def get_donators(self, obj):
        return ", ".join([dn.name for dn in obj.donator.all()])
    get_donators.short_description = _('donator')


admin.site.register(Donator, DonatorAdmin)
admin.site.register(Book, BookAdmin)
