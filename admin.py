import re
from datetime import datetime

from django.contrib import admin
from django.db.models import Max, Sum
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.admin import GenericTabularInline

from imagekit.admin import AdminThumbnail
from daterange_filter.filter import DateRangeFilter

from actions import merge_selected_donor
from models import *
from adli.admin_actions import (clone_action,
                                merge_selected_action,
                                export_csv_action)


class BookInline(admin.TabularInline):
    model = Book.donor.through
    readonly_fields = ["book_name", "book_donate_date", "book_amount"]
    raw_id_fields = ("book",)
    ordering = ["-book__donate_date"]
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


class DonorAdmin(admin.ModelAdmin):
    list_display = ["name",
                    "last_donate_date",
                    "amount",
                    "description",
                    "contact_info"]
    search_fields = ['name', 'description']
    list_filter = (('book__donate_date', DateRangeFilter),)
    inlines = [BookInline]
    actions = [merge_selected_action(function=merge_selected_donor),
               export_csv_action(fields=[
                   ('name', _('donor name')),
                   ('amount', _('amount')),
                   ('contact_info', _('contact info'))
               ])]
    exclude = ['name_index']

    def get_ordering(self, request):
        # only use the last_donate_date when in donor admin list
        path_info = request.META['PATH_INFO']
        print path_info
        if re.match(r'.*admin.*donor', path_info):
            return ['-last_donate_date', '-id']
        else:
            return ['name']

    def get_queryset(self, request):
        queryset = super(DonorAdmin, self).get_queryset(request)
        queryset = queryset.annotate(amount=Sum('book__amount'),
                                     last_donate_date=Max('book__donate_date'))
        return queryset

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


class PhotoInline(GenericTabularInline):
    model = Photo
    readonly_fields = ['admin_thumbnail']
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')

    admin_thumbnail.short_description = _('Thumbnail')


class LogInline(admin.TabularInline):
    model = Log
    readonly_fields = ['operator', 'time']

    def save_model(self, request, obj, form, change):
        obj.operator = request.user
        super(LogInline, self).save(request, obj, form, change)


class BookAdmin(admin.ModelAdmin):
    list_display = ["name",
                    "author_name",
                    "amount",
                    "donate_date",
                    "get_donors",
                    "last_modify_by",
                    "last_modify_date",
                    "publish",
                    "get_recent_logs"]
    search_fields = ['name', "author_name", "donor__name", "donate_date",
                     'log__description']
    filter_horizontal = ['donor']
    list_filter = (('donate_date', DateRangeFilter),
                   ('donor__name'),
                   ('book_type__name'),
                   ('batch__name'),
                   ('publish'),
                   ('last_modify_by__username'),
                   )
    actions = [
        export_csv_action(fields=['name', 'amount', 'donate_date', ],
                          extra=['get_donors']),
        clone_action()
        ]
    inlines = [LogInline, PhotoInline]
    exclude = ['last_modify_by']

    def save_model(self, request, obj, form, change):
        obj.last_modify_by = request.user
        obj.last_modify_date = datetime.now()
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            # Check if it is the correct type of inline
            if isinstance(instance, Log):
                if not instance.operator_id:
                    instance.operator = request.user

                instance.save()

    def construct_change_message(self, request, form, formsets):
        message = super(BookAdmin, self).construct_change_message(request,
                                                                  form,
                                                                  formsets)
        for item in form.changed_data:
            message += "\n%s => %s" % (item,
                                       unicode(form.cleaned_data.get(item)))

        return message

    def clone(self, obj, request):
        new_kwargs = dict()
        exclude = ['id', 'photos', 'last_modify_by', 'last_modify_date']
        for fld in self.model._meta.fields:
            if fld.name not in exclude:
                new_kwargs[fld.name] = getattr(obj, fld.name)

        new_kwargs['last_modify_by'] = request.user
        new_kwargs['last_modify_date'] = datetime.now()

        new_book = Book(**new_kwargs)
        new_book.save()
        new_book.donor.add(*obj.donor.values_list('id', flat=True))


class PhotoAdmin(admin.ModelAdmin):
    list_display = ["name", "admin_thumbnail"]
    fields = ["name", "image", "admin_thumbnail"]
    readonly_fields = ['admin_thumbnail']
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')
    search_fields = ['name']

    admin_thumbnail.short_description = _('Thumbnail')


admin.site.register(Donor, DonorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookType)
admin.site.register(Batch)
#admin.site.register(Photo, PhotoAdmin)
