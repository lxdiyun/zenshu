from django import forms
from django.core.paginator import Paginator
from zenshu.models import Donator, Book
from zenshu.utils import DONATOR_PAGE_SIZE
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _


class DonatorListPageForm(forms.Form):
    page = forms.IntegerField()

    def clean(self):
        cleaned_data = super(DonatorListPageForm, self).clean()
        paginator = Paginator(Donator.objects.all(), DONATOR_PAGE_SIZE)

        try:
            paginator.page(cleaned_data["page"])
        except:
            cleaned_data["page"] = "1"

        return cleaned_data


class DonatorSearchForm(forms.Form):
    keyword = forms.CharField(max_length=20)


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
