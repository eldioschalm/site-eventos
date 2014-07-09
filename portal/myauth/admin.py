# coding: utf-8

from django.contrib import admin
from portal.myauth.models import UserExtended
from django.utils.translation import ugettext_lazy as _


class UserExtendedAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email')

    def full_name(self, obj):
        return obj.get_full_name()

    full_name.short_description = _(u'Nome Completo')

admin.site.register(UserExtended, UserExtendedAdmin)
