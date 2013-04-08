from zenshu.models import Book, Donor, Photo
from zenshu.actions import merge_selected, export_csv_action
from zenshu.filters import DonorAnnotateFilter
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from daterange_filter.filter import DateRangeFilter
from django.contrib.contenttypes import generic
from imagekit.admin import AdminThumbnail
from adli.admin_actions import clone_action


class BookInline(admin.TabularInline):
    model = Book.donor.through
    readonly_fields = ["book_name", "book_donate_date", "book_amount"]
    ordering = ["-book__donate_date"]
    verbose_name = _("book")
    verbose_name_plural = _("book")
    raw_id_fields = ("book",)

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


class DonorAdmin(admin.ModelAdmin):
    list_display = ["name",
                    "last_donate_date",
                    "amount",
                    "description",
                    "contact_info"]
    search_fields = ['name', 'description']
    list_filter = (('book__donate_date', DateRangeFilter),
                   # Need this special filter to provide annotate field
                   # because the m2m annotation must after m2m filter
                   ('id', DonorAnnotateFilter))
    inlines = [BookInline]
    actions = [merge_selected,
               export_csv_action(fields=[
                   ('name', _('donor name')),
                   ('amount', _('amount')),
                   ('contact_info', _('contact info'))
               ])]

    def get_ordering(self, request):
        return ["-last_donate_date"]

    def last_donate_date(self, obj):
        return obj.last_donate_date
    last_donate_date.admin_order_field = 'last_donate_date'
    last_donate_date.short_description = _('last donate date')

    def amount(self, obj):
        return obj.amount
    amount.admin_order_field = 'amount'
    amount.short_description = _('amount')

    def lookup_allowed(self, lookup, value):
        if lookup in ('book__donate_date__lte', 'book__donate_date__gte'):
            return True
        return super(DonorAdmin, self).lookup_allowed(lookup, value)


class PhotoInline(generic.GenericTabularInline):
    model = Photo
    readonly_fields = ['admin_thumbnail']
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')

    admin_thumbnail.short_description = _('Thumbnail')


class BookAdmin(admin.ModelAdmin):
    list_display = ["name",
                    "author_name",
                    "amount",
                    "donate_date",
                    "get_donors"]
    search_fields = ['name', "author_name", "donor__name", "donate_date"]
    filter_horizontal = ['donor']
    list_filter = (('donate_date', DateRangeFilter),)
    actions = [export_csv_action(fields=[
        ('name', _('book name')),
        ('amount', _('amount')),
        ('donate_date', _('donate date')),
        ('get_donors', _('donor name'))]),
        clone_action()]
    inlines = [PhotoInline]

    def clone(self, obj, request):
        new_kwargs = dict()
        exclude = ['id', 'photos']
        for fld in self.model._meta.fields:
            if fld.name not in exclude:
                new_kwargs[fld.name] = getattr(obj, fld.name)

        self.model.objects.create(**new_kwargs)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ["name", "admin_thumbnail"]
    fields = ["name", "image", "admin_thumbnail"]
    readonly_fields = ['admin_thumbnail']
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')
    search_fields = ['name']

    admin_thumbnail.short_description = _('Thumbnail')


admin.site.register(Donor, DonorAdmin)
admin.site.register(Book, BookAdmin)
#admin.site.register(Photo, PhotoAdmin)
