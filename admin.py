from zenshu.models import Book, Donator
from django.contrib import admin
from django.db.models import Max


class DonatorAdmin(admin.ModelAdmin):
    list_display = ["name", "last_donate_date"]

    def queryset(self, request):
        qs = super(DonatorAdmin, self).queryset(request)
        return qs.annotate(last_donate_date=Max('book__donate_date'))

    def last_donate_date(self, obj):
        return obj.last_donate_date

    last_donate_date.admin_order_field = 'last_donate_date'

class BookAdmin(admin.ModelAdmin):
    list_display = ["name", "author_name", "amount", "donate_date"]

admin.site.register(Book, BookAdmin)
admin.site.register(Donator, DonatorAdmin)
