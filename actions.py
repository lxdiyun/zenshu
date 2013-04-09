from zenshu.models import Donor
from zenshu.transport import merge_dn
from django.utils.encoding import force_unicode


def merge_selected_donor(modeladmin, request, queryset):
    if (queryset and (1 < queryset.all().count())):
        key_dn = Donor()
        key_dn.name = queryset[0].name
        key_dn.save()

        for dn in queryset:
            merge_dn(key_dn, dn)
            dn_display = force_unicode(dn)
            modeladmin.log_deletion(request, dn, dn_display)

        key_dn.save()
        modeladmin.log_addition(request, key_dn)

        queryset.all().delete()
        return True
    else:
        return False
