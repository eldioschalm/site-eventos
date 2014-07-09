# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django import forms
from portal.myauth.models import UserExtended
from django.forms.fields import CharField # import for CPFField
from django.core.validators import EMPTY_VALUES # import for CPFField
from django.core.validators import ValidationError # import for CPFField
import re # import for CPFField


class CPFField(CharField):
    """
    This field validate a CPF number or a CPF string. A CPF number is
    compounded by XXX.XXX.XXX-VD. The two last digits are check digits.

    More information:
    http://en.wikipedia.org/wiki/Cadastro_de_Pessoas_F%C3%ADsicas
    """
    default_error_messages = {
        'invalid': _("Invalid CPF number."),
        'max_digits': _("This field requires at most 11 digits or 14 characters."),
        'digits_only': _("This field requires only numbers."),
    }

    def DV_maker(self, v):
        if v >= 2:
            return 11 - v
        return 0

    def __init__(self, max_length=14, min_length=11, *args, **kwargs):
        super(CPFField, self).__init__(max_length, min_length, *args, **kwargs)

    def clean(self, value):
        """
        Value can be either a string in the format XXX.XXX.XXX-XX or an
        11-digit number.
        """
        value = super(CPFField, self).clean(value)
        if value in EMPTY_VALUES:
            return ''

        if not value.isdigit():
            value = re.sub("[-\.]", "", value)
        try:
            int(value)
        except ValueError:
            raise ValidationError(self.error_messages['digits_only'])

        if len(value) != 11:
            raise ValidationError(self.error_messages['max_digits'])

        orig_dv = value[-2:]

        new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(10, 1, -1))])
        new_1dv = self.DV_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1))])
        new_2dv = self.DV_maker(new_2dv % 11)
        value = value[:-1] + str(new_2dv)
        if value[-2:] != orig_dv:
            raise ValidationError(self.error_messages['invalid'])

        return value


class UserCreationForm(forms.ModelForm):
    cpf = CPFField(help_text='11 dígitos ou no formato XXX.XXX.XXX-XX')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label=_(u'Confirme a senha'))
    class Meta:
        model = UserExtended
        fields = ('username', 'first_name', 'last_name', 'email', 'cpf', 'phone', 'password',)

    def __init__(self, *args, **kwargs):
        self.base_fields['first_name'].label = u'Primeiro nome'
        self.base_fields['last_name'].label = u'Sobrenome completo'
        self.base_fields['password'].help_text = u'Informe uma senha segura'
        self.base_fields['confirm_password'].help_text = u'Informe a senha novamente'
        self.base_fields['password'].widget = forms.PasswordInput()
        super(UserCreationForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        return self.cleaned_data['username'].lower()

    def clean_email(self):
        if UserExtended.objects.filter(email=self.cleaned_data['email'],).count():
            raise forms.ValidationError(u'e-mail já cadastrado')

        return self.cleaned_data['email'].lower()

    def clean_confirm_password(self):
        if self.cleaned_data['confirm_password'] != self.data['password']:
            raise forms.ValidationError('Senhas não conferem!')

        return self.cleaned_data['confirm_password']

    def string_capitalize(self, string):
        lstring = []
        prep = ("da","de","di","do","du","das","dos","e")
        for i in string.lower().split():
            if i not in prep:
                i = i.capitalize()
            lstring.append(i)
        return ' '.join(lstring)

    def clean_first_name(self):
        return self.string_capitalize(self.cleaned_data['first_name'])

    def clean_last_name(self):
        return self.string_capitalize(self.cleaned_data['last_name'])

    def save(self, commit=True):
        useradd = super(UserCreationForm, self).save(commit=False)

        useradd.set_password(self.cleaned_data['password'])

        if commit:
            useradd.save()

        return useradd

class UserSettingsForm(forms.ModelForm):
    cpf = CPFField(help_text='11 dígitos ou no formato XXX.XXX.XXX-XX')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label=_(u'Confirme a senha'))
    class Meta:
        model = UserExtended
        fields = ('username', 'first_name', 'last_name', 'email', 'cpf', 'phone', 'password',)

    def __init__(self, *args, **kwargs):
        self.base_fields['first_name'].label = u'Primeiro nome'
        self.base_fields['last_name'].label = u'Sobrenome completo'
        self.base_fields['password'].help_text = u'Informe uma senha segura'
        self.base_fields['confirm_password'].help_text = u'Informe a senha novamente'
        self.base_fields['password'].widget = forms.PasswordInput()
        super(UserSettingsForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        return self.cleaned_data['username'].lower()

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        if email and UserExtended.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email.lower()

        return self.cleaned_data['email'].lower()

    def clean_confirm_password(self):
        if self.cleaned_data['confirm_password'] != self.data['password']:
            raise forms.ValidationError('Senhas não conferem!')

        return self.cleaned_data['confirm_password']

    def string_capitalize(self, string):
        lstring = []
        prep = ("da","de","di","do","du","das","dos","e")
        for i in string.lower().split():
            if i not in prep:
                i = i.capitalize()
            lstring.append(i)
        return ' '.join(lstring)

    def clean_first_name(self):
        return self.string_capitalize(self.cleaned_data['first_name'])

    def clean_last_name(self):
        return self.string_capitalize(self.cleaned_data['last_name'])

    def save(self, commit=True):
        user_update = super(UserSettingsForm, self).save(commit=False)

        user_update.set_password(self.cleaned_data['password'])

        if commit:
            user_update.save()

        return user_update