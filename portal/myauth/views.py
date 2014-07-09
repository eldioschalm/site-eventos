# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from portal.myauth.forms import UserCreationForm
from portal.myauth.forms import UserSettingsForm
from portal.myauth.models import UserExtended
from django.shortcuts import get_object_or_404

def user_creation(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/events/')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/user_creation.html', locals(),)

def user_settings(request):
    if request.POST:
        user = get_object_or_404(UserExtended, id=request.user.id)
        form = UserSettingsForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/events/')
    else:
        user = get_object_or_404(UserExtended, id=request.user.id)
        form = UserSettingsForm(instance=user)

    return render(request, 'accounts/user_settings.html', locals(),)