from zenshu.models import Donator
from zenshu.transport import merge_dn
from zenshu.utils import UnicodeWriter
from django.utils.translation import ugettext_lazy as _
#from django.utils.safestring import mark_safe
#from django.http import HttpResponseRedirect
#from django.shortcuts import render_to_response
#from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
#from django.utils.encoding import smart_str, smart_unicode


def merge_selected_donators(self, request, queryset):
    if (queryset and (1 < queryset.all().count())):
        key_dn = Donator()
        key_dn.name = queryset[0].name
        key_dn.save()

        for dn in queryset:
            merge_dn(key_dn, dn)

        key_dn.save()
        queryset.all().delete()
        messages.success(request, _("Merge Completed"))
    else:
        messages.error(request, _("Please select at least two donators"))

merge_selected_donators.short_description = _("Merge selected")


def prep_field(obj, field):
    """ Returns the field as a unicode string. If the field is a callable, it
    attempts to call it first, without arguments.
    """
    if '__' in field:
        bits = field.split('__')
        field = bits.pop()

        for bit in bits:
            obj = getattr(obj, bit, None)

            if obj is None:
                return ""

    attr = getattr(obj, field)
    output = attr() if callable(attr) else attr
#    return unicode(output).encode('utf-8') if output else ""
    return output


def export_csv_action(description=_("Export Selected"),
                      fields=None,
                      exclude=None,
                      header=True):
    """ This function returns an export csv action. """
    def export_as_csv(modeladmin, request, queryset):
        """ Generic csv export admin action.
        Based on http://djangosnippets.org/snippets/2712/
        """
        opts = modeladmin.model._meta
        field_names = [field.name for field in opts.fields]
        labels = []

        if exclude:
            field_names = [f for f in field_names if f not in exclude]

        elif fields:
            field_names = [field for field, _ in fields]
            labels = [label for _, label in fields]

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % (
            unicode(opts).replace('.', '_')
        )

        writer = UnicodeWriter(response)

        if header:
            writer.writerow(labels if labels else field_names)

        for obj in queryset:
            writer.writerow([prep_field(obj, field) for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv
