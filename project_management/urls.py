# -*- coding: utf-8 -*-

# Django Imports
from django.conf.urls import url

# Project Imports
from project_management.views import create_custom_list

urlpatterns = [
    url(r'^create_list/$', create_custom_list, name='create_custom_list'),
]
