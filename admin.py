from zenshu.models import Book, Donator
from django.contrib import admin
from django.db.models import Max
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _


class DonatorAdminForm(forms.ModelForm):
    book = forms.ModelMultipleChoiceField(
        queryset=Book.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('book'),
            is_stacked=False
        ),
        label=_('book')
    )

    class Meta:
        model = Donator

    def __init__(self, *args, **kwargs):
        super(DonatorAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['book'].initial = self.instance.book_set.all()

    def save(self, commit=True):
        donator = super(DonatorAdminForm, self).save(commit=False)

        if commit:
            donator.save()

        if donator.pk:
            donator.book_set = self.cleaned_data['book']
            self.save_m2m()

        return donator


class DonatorAdmin(admin.ModelAdmin):
    list_display = ["name", "last_donate_date", "description"]
    search_fields = ['name', "description"]
    list_filter = ["book__donate_date"]
    form = DonatorAdminForm

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
