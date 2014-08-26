# coding: utf-8

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
#from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
import datetime
from portal.events.models import Event
from portal.events.models import Programation
from portal.events.models import ProgramationUserExtended
from portal.myauth.models import UserExtended
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _
# import json # json para usar no select com ajax
from django.utils import simplejson
from django.http import HttpResponse
import csv # para gerar relatorio csv


@login_required(login_url='/accounts/login/')
def events_list(request):
    events = Event.objects.filter(inscription_start__lte=datetime.date.today(), inscription_end__gte=datetime.date.today())
    #lte <= date
    #gte >= date
    return render(request, 'events/index.html', locals())


def events_detail(request, id):
    if request.method == 'POST':
        message = []
        if request.POST.getlist('programation'):
            user = UserExtended.objects.get(id=request.user.id)
            for c in request.POST.getlist('programation'):
                try:
                    prog = Programation.objects.get(id=int(c))
                    # p_count = p.userextended.through.objects.exclude(modality='AP').count()
                    prog_count = ProgramationUserExtended.objects.filter(programation=prog.id, modality='PA').count()
                    if (prog.vacancies > 0) and (prog_count < prog.vacancies):
                        obj = ProgramationUserExtended(programation_id=int(c), userextended=user, modality='PA')
                        obj.save()
                        string_translate = (_(u'Registration held successfully for '))
                        message.append(u'{0} {1}.'.format(string_translate, prog.name))
                    else:
                        message.append(u'vagas esgotadas')
                        # message.append(_(u'No programming available'))
                except IntegrityError:
                    # if unique_toguether make a exception
                    string_translate = (_(u'Reregistration found for '))
                    message.append(u'{0} {1}.'.format(string_translate, prog.name))
            link_name = _(u'List programmings')
            link_href = request.get_full_path()
            return render(request, 'events/message.html', locals())
        else:
            message.append(_(u'No programming list for registration.'))
            link_name = _(u'List programmings')
            link_href = request.get_full_path()
            return render(request, 'events/message.html', locals())
    else:
        event = get_object_or_404(Event, id=id)
        programation_all = event.programation_set.all()
        entries_made = ProgramationUserExtended.objects.filter(userextended=request.user, programation__in=programation_all)  # , programation in programation_all) # programation_id in programation) # for list programmings entries made of user
        programation = event.programation_set.exclude(programationuserextended__in=entries_made)
        return render(request, 'events/events_detail.html', locals())

def entries_made_exclude(request, event, programationuserextended): # delete record ProgramationUserExtended
    message = []
    try:
        obj = get_object_or_404(ProgramationUserExtended, id=programationuserextended)
        obj.delete()

        message.append(_(u'Programming successfully deleted.'))
        link_name = _(u'List of programmings')
        link_href = '/events/{0}/'.format(event)
        return render(request, 'events/message.html', locals())
    except:
        message.append(_(u'Error, record does not exist.'))
        link_name = _(u'List of programmings')
        link_href = '/events/{0}/'.format(event)
        return render(request, 'events/message.html', locals())


def json(request, event_id):
    queryset = Programation.objects.filter(event=event_id).values_list('id', 'name')
    dados = dict(queryset)
    return HttpResponse(simplejson.dumps(dados), mimetype="application/json")


def paralista(line):
    lista = []
    for l in line:
        try:
            lista.append(l.encode('utf8'))
        except:
            lista.append(l)
    return lista


@permission_required('events.change_programation')
def report(request):
    try:
        queryset = ProgramationUserExtended.objects.select_related().filter(programation=request.POST['programation']).values_list('userextended__username', 'userextended__first_name', 'userextended__last_name', 'userextended__email', 'userextended__cpf', 'userextended__phone', 'participated')
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Usuário', 'nome', 'sobrenome', 'email', 'cpf', 'telefone', 'participou'])
        for q in queryset:
            writer.writerow(paralista(q))

        return response
    except KeyError:
        queryset = Event.objects.all().values('id', 'name')
        return render(request, 'events/events_report.html', {'queryset': queryset})


@permission_required('events.change_programation')
def reportfull(request):
    queryset = ProgramationUserExtended.objects.select_related().values_list('userextended__username', 'userextended__first_name', 'userextended__last_name', 'userextended__email', 'userextended__cpf', 'userextended__phone', 'participated', 'programation__name')
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reportfull.csv"'

    writer = csv.writer(response)
    writer.writerow(['Usuário', 'nome', 'sobrenome', 'email', 'cpf', 'telefone', 'participou', 'programação'])
    for q in queryset:
        writer.writerow(paralista(q))

    return response


#print request.user.get_all_permissions()
# @permission_required('events.change_programation')
# def generate_csv(request):
#     import csv
#     from django.http import HttpResponse
#
#     event = Event.objects.get(id=1)
#     programation = event.programation_set.get(id=1)
#     users = ProgramationUserExtended.objects.filter(programation=programation)
#
#     # Create the HttpResponse object with the appropriate CSV header.
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="inscritos.csv"'
#
#     writer = csv.writer(response)
#     writer.writerow(['Nome dos Inscritos'])
#     for u in users:
#         writer.writerow([u])
#
#     return response
#
# @permission_required('events.change_programation')
# def generate_participants(request):
#     import csv
#     from django.http import HttpResponse
#
#     event = Event.objects.get(id=1)
#     programation = event.programation_set.get(id=1)
#     users = ProgramationUserExtended.objects.filter(programation=programation, participated=True)
#
#     # Create the HttpResponse object with the appropriate CSV header.
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="participants.csv"'
#
#     writer = csv.writer(response)
#     writer.writerow(['Participantes'])
#     for u in users:
#         writer.writerow([u])
#
#     return response


@permission_required('events.change_programation')
def without(request):
    from django.http import HttpResponse
    entries_made = ProgramationUserExtended.objects.all()
    users = UserExtended.objects.exclude(programationuserextended__in=entries_made)

    output = '\n<br /> '.join([u.get_full_name() + ' &lt;' + u.email + '&gt;,' for u in users])

    return HttpResponse(output)

#example of view for multiples args
#def some_view(request, *args, **kwargs):
#    if kwargs.get('q', None):