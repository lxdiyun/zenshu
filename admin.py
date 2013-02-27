from zenshu.models import Book, Donator
from django.contrib import admin
from django.db.models import Max
from django.utils.translation import ugettext_lazy as _


class BookInline(admin.TabularInline):
    model = Book.donator.through
    verbose_name = _('book')

class DonatorAdmin(admin.ModelAdmin):
    list_display = ["name", "last_donate_date", "description"]
    search_fields = ['name', "description"]
    list_filter = ["book__donate_date"]
    inlines = [BookInline,]

    def queryset(self, request):
        qs = super(DonatorAdmin, self).queryset(request)
        return qs.annotate(last_donate_date=Max('book__donate_date'))

    def last_donate_date(self, obj):
        return obj.last_donate_date

    last_donate_date.admin_order_field = 'last_donate_date'
    last_donate_date.short_description = _('last donate date')

class BookAdmin(admin.ModelAdmin):
    list_display = ["name", "author_name", "amount", "donate_date"]
    search_fields = ['name', "author_name"]
    filter_horizontal = ['donator']
    list_filter = ['donate_date']

admin.site.register(Donator, DonatorAdmin)
admin.site.register(Book, BookAdmin)
