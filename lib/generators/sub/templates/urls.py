# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from rest_framework import routers

urlpatterns = patterns(
    '',
)

router = routers.DefaultRouter()

urlpatterns += patterns('', url(r'^api/', include(router.urls)))