from django import forms
from django.core.paginator import Paginator
from zenshu.models import Donator
from zenshu.utils import DONATOR_PAGE_SIZE


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
