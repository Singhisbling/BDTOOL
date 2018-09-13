# -*- coding: utf-8 -*-

# Django Imports
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect

# Project Imports
from project_management.forms import ListForm
from project_management.models import List


@csrf_protect
def create_custom_list(request):
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            project_list = List()
            project_list.name = form.cleaned_data['name']
            project_list.created_by = request.user
            project_list.updated_by = request.user
            project_list.save()

            count = 0
            for project in request.session.get('data'):
                project_list.projects.add(project)
                count += 1

            messages.add_message(
                request, messages.INFO,
                "Successfully added {} projects to list {}.".format(
                    count, project_list.name
                )
            )
            return HttpResponseRedirect("/admin/project_management/list/")
