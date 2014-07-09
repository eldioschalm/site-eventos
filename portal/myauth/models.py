# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserExtended(User):
    '''
    class to add a field CPF and phone into a user db
    '''
    cpf = models.CharField(_(u'CPF'), max_length=11, unique=True)
    phone = models.CharField(_(u'Phone'), max_length=20, blank=True)