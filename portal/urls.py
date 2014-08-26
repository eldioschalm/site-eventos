# coding: utf-8

from django.conf.urls import patterns, include, url
#from django.contrib.auth.views import password_reset


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'portal.views.home', name='home'),
    # url(r'^portal/', include('portal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
#)

urlpatterns = patterns('',
    url(r'^$', 'portal.core.views.landingpage', name='landingpage'),
    url(r'^events/$', 'portal.events.views.events_list', name='events_list'),
    url(r'^events/(?P<id>\d+)/$', 'portal.events.views.events_detail', name='events_detail'),
    url(r'^events/(?P<event>\d+)/(?P<programationuserextended>\d+)/$', 'portal.events.views.entries_made_exclude', name='entries_made_exclude'),
    # for admin
    url(r'^admin/', include(admin.site.urls)),
    # relatorio para usuários cadastrados sem inscricao
    url(r'^events/without/$', 'portal.events.views.without', name='without'),
    # json para report
    url(r'^events/report/$', 'portal.events.views.report', name='report'),
    # relatorio completo
    url(r'^events/reportfull/$', 'portal.events.views.reportfull', name='reportfull'),
    # json para relatorio
    url(r'^json/(?P<event_id>\d+)/$', 'portal.events.views.json', name='json'),
    # login
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    # logout
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    # user creation
    url(r'^user_creation/$', 'portal.myauth.views.user_creation', {}, name='user_creation'),
    # user profile
    url(r'^accounts/user_settings/$', 'portal.myauth.views.user_settings', {}, name='user_settings'),

    #password_reset
    (r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset',
            {'template_name': 'accounts/password_reset_form.html', 'post_reset_redirect': '/accounts/password/reset/done/'}),
    (r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done',
            {'template_name': 'accounts/password_reset_done.html'}),
    (r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',
            {'template_name': 'accounts/password_reset_confirm.html', 'post_reset_redirect': '/accounts/password/done/'}),
    (r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete',
            {'template_name': 'accounts/password_reset_complete.html'}),
    #password_reset end
)
