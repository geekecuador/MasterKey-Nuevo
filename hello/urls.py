"""hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login,logout
from estudiante import views
from hello import settings
from estudiante.views import Busqueda_info_ajax

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login),
    url(r'^rank/$', 'estudiante.views.academirank',name='academirank'),
	url(r'^accounts/logout/$', logout),
    url(r'^login/','estudiante.views.login_user',name='login_user'),
    url(r'^(?:signin.html)?$','estudiante.views.login_user',name='login'),
    url(r'^logout/$', login),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^info_ajax/$',Busqueda_info_ajax.as_view()),
    url(r'^taller/(?P<pullo>\d+)$', 'estudiante.views.update', name='update'),
    url(r'^reserva-taller/$', views.reserva),
    url(r'^reserva-curso/$', views.reservar_curso),
    # url(r'^buscar/$', views.buscar),
    # url(r'^talleres/', 'estudiante.views.reservaTaller', name='reservaTaller'),
]

