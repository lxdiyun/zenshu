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
    
class DonatorSearchForm(forms.Form):
    keyword = forms.CharField(max_length=20)

    def is_valid(self):
        if (super(DonatorSearchForm, self).is_valid()
            and "" != self.cleaned_data['keyword']):
            return True
            
        return False
