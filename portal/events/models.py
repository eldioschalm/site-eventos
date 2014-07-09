#coding: utf-8

from django.db import models
from portal.myauth.models import UserExtended
from django.utils.translation import ugettext_lazy as _

class Campi(models.Model):
    name = models.CharField(_(u'nome'), max_length=255)

    class Meta:
        verbose_name = _(u'campus')
        verbose_name_plural = _(u'campi')

    def __unicode__(self):
        return self.name


class Sector(models.Model):
    campi = models.ForeignKey(Campi, verbose_name=_(u'campi'))
    name = models.CharField(_(u'nome'), max_length=255)

    class Meta:
        verbose_name = _(u'setor')
        verbose_name_plural = _(u'setores')

    def __unicode__(self):
        return self.name


class Event(models.Model):
    sector = models.ForeignKey(Sector, verbose_name=_(u'setor'))
    name = models.CharField(_(u'nome'), max_length=255)
    date_start = models.DateField(_(u'data de início'))
    date_end = models.DateField(_(u'data de encerramento'))
    inscription_start = models.DateField(_(u'início das inscrições'))
    inscription_end = models.DateField(_(u'encerramento das inscrições'))

    class Meta:
        verbose_name = _(u'evento')
        verbose_name_plural = _(u'eventos')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/events/%i/' % self.id


class Programation(models.Model):
    event = models.ForeignKey(Event, verbose_name=_(u'evento'))
    userextended = models.ManyToManyField(UserExtended, \
                                          through='ProgramationUserExtended', \
                                          verbose_name=_(u'participante'), blank=True)
    name = models.CharField(_(u'nome'), max_length=255)
    description = models.TextField(_(u'descrição'), blank=True)
    date_start = models.DateField(_(u'data de início'))
    date_end = models.DateField(_(u'data de encerramento'))
    time_start = models.TimeField(_(u'hora de início'))
    time_end = models.TimeField(_(u'hora de encerramento'))
    vacancies = models.IntegerField(u'número de vagas')

    class Meta:
        verbose_name = _(u'programação')
        verbose_name_plural = _(u'programações')

    def __unicode__(self):
        return 'Evento: ' + self.event.name + '/' + self.name

    def get_inscribes(self):
        return self.userextended.through.objects.exclude(modality='AP').count()


class ProgramationUserExtended(models.Model):
    KINDS = (
        ('AP', _(u'Apresentador')),
        ('PA', _(u'Participante')),
    )
    programation = models.ForeignKey(Programation, verbose_name=_(u'programação'))
    userextended = models.ForeignKey(UserExtended, verbose_name=_(u'participante'))
    participated = models.BooleanField(_(u'participou'))
    modality = models.CharField(_('Modalidade'), max_length=2, choices=KINDS, default='PA')

    class Meta:
        verbose_name = _(u'participante')
        verbose_name_plural = _(u'participantes')
        unique_together = (('programation', 'userextended'),)

        #permissions = (
        #     ('generate_label', u'gerar etiquetas'),
        #)

    def __unicode__(self):
        return self.userextended.get_full_name()

