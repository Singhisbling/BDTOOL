# -*- coding: utf-8 -*-

# Python Imports
import csv

# Django Imports
from django import forms
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from mptt.admin import DraggableMPTTAdmin

# Project Imports
from import_export.admin import ImportExportModelAdmin
from project_management.forms import ListForm
from project_management.models import (
    Client, Domain, List, Project, Tags, Technology
)
from project_management.filters import (
    BudgetRangeFilter, CurrencyTypeFilter, DropdownFilter,
    RelatedDropdownFilter
)
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from search_admin_autocomplete.admin import SearchAutoCompleteAdmin


class ExportExcelMixin:
    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = (
            'attachment; filename={}.xlsx'.format(
                meta
            )
        )
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow(
                [getattr(obj, field) for field in field_names]
            )
        return response

    export_as_excel.short_description = (
        "Export selected %(verbose_name_plural)s"
    )


class ClientAdmin(ImportExportModelAdmin, ExportExcelMixin):
    model = Client
    fieldsets = (
        ('Personal info', {
            'fields': (
                ('first_name', 'last_name'), ('email', 'phone_number'),
            )
        }),
        ('Other details', {
            'fields': (
                ('skype_id', 'country'), 'platform', 'feedback',
            )
        }),
        ('Status', {
            'fields': (
                'active',
            )
        }),
    )

    list_filter = (
        ('email', DropdownFilter), ('skype_id', DropdownFilter),
        ('country', DropdownFilter),
        'active', ('created_by', RelatedDropdownFilter),
        ('updated_by', RelatedDropdownFilter),
        ('created_on', DateTimeRangeFilter),
        ('updated_on', DateTimeRangeFilter),
    )

    list_display = (
        'first_name', 'last_name', 'skype_id', 'email', 'phone_number',
        'country', 'platform', 'short_feedback', 'active', 'created_by',
        'updated_by',
    )

    search_fields = [
        'first_name', 'last_name', 'email', 'skype_id', 'platform', 'feedback'
    ]

    actions = ["export_as_excel"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()


class DomainAdmin(DraggableMPTTAdmin):
    model = Domain
    fieldsets = (
        (None, {
            'fields': (
                'name', 'parent', 'active',
            )
        }),
    )

    list_filter = (
        ('name', DropdownFilter), ('parent', RelatedDropdownFilter), 'active',
    )

    list_display = ('tree_actions', 'indented_title', 'active',)

    list_display_links = ('indented_title',)

    search_fields = ['name']


class ListAdmin(SearchAutoCompleteAdmin):
    model = List
    fieldsets = (
        (None, {
            'fields': (
                'name', 'projects',
            )
        }),
    )

    filter_horizontal = ('projects',)

    list_filter = (
        ('name', DropdownFilter), ('projects', RelatedDropdownFilter),
        ('created_on', DateTimeRangeFilter),
        ('updated_on', DateTimeRangeFilter),
    )

    list_display = ('name', '_projects', 'created_by', 'updated_by',)

    search_fields = ['name']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()


class ProjectAdmin(ImportExportModelAdmin, ExportExcelMixin):
    model = Project
    fieldsets = (
        ('Project details', {
            'fields': (
                ('name', 'url'), 'mobile_url',
                ('client', 'project_type', 'project_status'),
                ('project_start_date', 'project_end_date'),
            )
        }),
        ('Budget details', {
            'fields': (
                'budget_type', 'project_budget',
            )
        }),
        ('Other details', {
            'fields': (
                ('technologies', 'domains'), 'tags',
                ('description', 'responsibilities'),
                ('attachments', 'logo', '_logo'),
                'demo_video_link', ('manager_name', 'team_members'),
                'additional_detail',
            )
        }),
    )

    filter_horizontal = ('domains', 'tags', 'technologies',)

    readonly_fields = ['_logo']

    raw_id_fields = ["client"]

    list_filter = (
        ('client', RelatedDropdownFilter), 'project_type', 'project_status',
        ('project_start_date', DateRangeFilter),
        ('project_end_date', DateRangeFilter), 'budget_type',
        CurrencyTypeFilter, BudgetRangeFilter,
        ('technologies', RelatedDropdownFilter),
        ('domains', RelatedDropdownFilter), ('tags', RelatedDropdownFilter),
        ('created_by', RelatedDropdownFilter),
        ('updated_by', RelatedDropdownFilter),
        ('created_on', DateTimeRangeFilter),
        ('updated_on', DateTimeRangeFilter),
    )

    list_display = (
        'name', '_client_detail', '_url', '_mobile_url', '_tags',
        '_technologies', 'project_type', 'project_status',
        'project_start_date', 'project_end_date', 'budget_type',
        'project_budget', '_demo_video_link', 'manager_name', 'team_members',
        'created_by', 'updated_by',
    )

    def create_list(self, request, queryset):
        form = ListForm()
        data = []
        for i in queryset:
            data.append(i.id)
            request.session['data'] = data
        return render(
            request, 'admin/project/create_list.html',
            {'form': form, 'projects': queryset}
        )

    create_list.short_description = "Create custom project list"

    actions = ["export_as_excel", create_list]

    search_fields = [
        'name', 'url', 'mobile_url', 'description', 'tags__name',
        'technologies__name'
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        # customize tags box size
        if db_field.name in ['tags']:
            kwargs['widget'] = forms.Textarea(attrs={'rows': 1, 'cols': 75})
        # customize description box size
        if db_field.name in ['description']:
            kwargs['widget'] = forms.Textarea(attrs={'rows': 6, 'cols': 40})
        # customize responsibilities box size
        if db_field.name in ['responsibilities']:
            kwargs['widget'] = forms.Textarea(attrs={'rows': 6, 'cols': 40})
        # customize additional_detail box size
        if db_field.name in ['additional_detail']:
            kwargs['widget'] = forms.Textarea(attrs={'rows': 6, 'cols': 40})
        # customize team_members box size
        if db_field.name in ['team_members']:
            kwargs['widget'] = forms.Textarea(attrs={'rows': 6, 'cols': 40})
        return super(ProjectAdmin, self).formfield_for_dbfield(
            db_field, **kwargs
        )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()


class TagsAdmin(SearchAutoCompleteAdmin):
    model = Tags

    list_filter = (('name', DropdownFilter),)

    list_display = ('name',)

    search_fields = ['name']


class TechnologyAdmin(SearchAutoCompleteAdmin):
    model = Technology

    list_filter = (('name', DropdownFilter), 'category',)

    list_display = ('name', 'category',)

    search_fields = ['name']


admin.site.register(Client, ClientAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(List, ListAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Technology, TechnologyAdmin)
