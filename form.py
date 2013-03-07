from django import forms
from django.core.paginator import Paginator
from zenshu.models import Donor, Book
from zenshu.utils import DONATOR_PAGE_SIZE
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _


class DonorListPageForm(forms.Form):
    page = forms.IntegerField()

    def clean(self):
        cleaned_data = super(DonorListPageForm, self).clean()
        paginator = Paginator(Donor.objects.all(), DONATOR_PAGE_SIZE)

        try:
            paginator.page(cleaned_data["page"])
        except:
            cleaned_data["page"] = "1"

        return cleaned_data


class DonorSearchForm(forms.Form):
    keyword = forms.CharField(max_length=20)


class DonorAdminForm(forms.ModelForm):
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
        model = Donor

    def __init__(self, *args, **kwargs):
        super(DonorAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['book'].initial = self.instance.book_set.all()

    def save(self, commit=True):
        donor = super(DonorAdminForm, self).save(commit=False)

        if commit:
            donor.save()

        if donor.pk:
            donor.book_set = self.cleaned_data['book']
            self.save_m2m()

        return donor
