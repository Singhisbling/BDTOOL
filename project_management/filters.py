# -*- coding: utf-8 -*-

# Django Imports
from django.contrib.admin.filters import (
    AllValuesFieldListFilter, ChoicesFieldListFilter, RelatedFieldListFilter,
    RelatedOnlyFieldListFilter
)
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class DropdownFilter(AllValuesFieldListFilter):
    template = 'admin/dropdown_filter.html'


class ChoiceDropdownFilter(ChoicesFieldListFilter):
    template = 'admin/dropdown_filter.html'


class RelatedDropdownFilter(RelatedFieldListFilter):
    template = 'admin/dropdown_filter.html'


class RelatedOnlyDropdownFilter(RelatedOnlyFieldListFilter):
    template = 'admin/dropdown_filter.html'


class BudgetRangeFilter(admin.SimpleListFilter):
    title = _('budget range')
    parameter_name = 'project_budget'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('0', _('Under 1,000')),
            ('1', _('1,000 - 5,000')),
            ('2', _('5,000 - 10,000')),
            ('3', _('10,000 - 15,000')),
            ('4', _('Over 15,000')),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(
                project_budget__gte=0, project_budget__lt=1000
            )

        if self.value() == "1":
            return queryset.filter(
                project_budget__gte=1000, project_budget__lt=5000
            )

        if self.value() == "2":
            return queryset.filter(
                project_budget__gte=5000, project_budget__lt=10000
            )

        if self.value() == "3":
            return queryset.filter(
                project_budget__gte=10000, project_budget__lt=15000
            )

        if self.value() == "4":
            return queryset.filter(project_budget__gte=15000)


class CurrencyTypeFilter(admin.SimpleListFilter):
    title = _('currency type')
    parameter_name = "project_budget_currency"

    def lookups(self, request, model_admin):
        return (
            ('EUR', _('Euro (€)')),
            ('INR',_('Indian Rupee (₹)')),
            ('USD',_('US Dollar ($)')),
        )

    def queryset(self, request, queryset):
        if self.value() == "INR":
            return queryset.filter(project_budget_currency='INR')
        if self.value() == "USD":
            return queryset.filter(project_budget_currency='USD')
        if self.value() == "EUR":
            return queryset.filter(project_budget_currency='EUR')
