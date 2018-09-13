# -*- coding: utf-8 -*-

# Django Imports
from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
from django.template.defaultfilters import truncatechars
from django.utils.html import format_html
from djmoney.models.fields import MoneyField
from mptt.models import MPTTModel
from phonenumber_field.modelfields import PhoneNumberField


BUDGET_TYPE = (
    (0, 'Hourly'),
    (1, 'Fixed'),
)

PROJECT_STATUS = (
    (0, 'Lead'),
    (1, 'In Communication'),
    (2, 'Closed (In Progress)'),
    (3, 'Not Pursue'),
    (4, 'Completed'),
)

PROJECT_TYPE = (
    (0, 'Mobile Application'),
    (1, 'Web Application'),
)

TECH_CATEGORY = (
    (0, 'Full Stack'),
    (1, 'Frontend'),
    (2, 'Backend'),
    (3, 'Database'),
)


class Client(models.Model):
    # Relations
    created_by = models.ForeignKey(
        User, related_name='created_clients', on_delete=models.CASCADE,
        default=1
    )
    updated_by = models.ForeignKey(
        User, related_name='updated_clients', on_delete=models.CASCADE,
        default=1
    )

    # Attributes
    active = models.BooleanField(default=True)

    country = CountryField()

    email = models.EmailField(unique=True, blank=True, null=True)

    first_name = models.CharField(
        max_length=200, blank=True, null=True, db_index=True
    )
    last_name = models.CharField(
        max_length=200, blank=True, null=True, db_index=True
    )
    platform = models.CharField(
        max_length=200, blank=True, null=True, db_index=True
    )
    skype_id = models.CharField(
        max_length=150, blank=True, null=True, db_index=True
    )

    feedback = models.TextField(blank=True, null=True)

    phone_number = PhoneNumberField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(
            self.first_name, self.last_name
        )

    @property
    def short_feedback(self):
        return truncatechars(self.feedback, 80)


class Domain(MPTTModel):
    # Relations
    parent = models.ForeignKey(
        'self', blank=True, null=True, default=None, on_delete=models.CASCADE,
        related_name='child_domain'
    )

    # Attributes
    active = models.BooleanField(default=True)

    name = models.CharField(max_length=255, db_index=True, unique=True)

    class MPTTMeta:
        parent_attr = 'parent'
        level_attr = 'mptt_level'
        order_insertion_by = ['name']
        ordering = ['tree_id', 'lft']

    def __str__(self):
        return self.name


class Tags(models.Model):
    # Attributes
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Technology(models.Model):
    # Attributes
    category = models.IntegerField(choices=TECH_CATEGORY, default=0)

    name = models.CharField(max_length=200, db_index=True, unique=True)

    class Meta:
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.name


class Project(models.Model):
    # Relations
    client = models.ForeignKey(
        Client, blank=True, null=True, on_delete=models.CASCADE
    )
    domains = models.ManyToManyField(Domain)
    tags = models.ManyToManyField(Tags, blank=True)
    technologies = models.ManyToManyField(Technology)

    created_by = models.ForeignKey(
        User, related_name='created_projects', on_delete=models.CASCADE,
        default=1
    )
    updated_by = models.ForeignKey(
        User, related_name='updated_projects', on_delete=models.CASCADE,
        default=1
    )

    # Attributes
    name = models.CharField(max_length=250, verbose_name='Project Name')
    manager_name = models.CharField(max_length=250, blank=True, null=True)

    additional_detail = models.TextField(blank=True, null=True)
    description = models.TextField()
    responsibilities = models.TextField(blank=True, null=True)
    team_members = models.TextField(blank=True, null=True)

    demo_video_link = models.URLField(blank=True, null=True)
    mobile_url = models.URLField(
        blank=True, null=True, verbose_name='Mobile URL'
    )
    url = models.URLField()

    attachments = models.FileField(blank=True, null=True, upload_to='')

    logo = models.ImageField(blank=True, null=True, upload_to='')

    project_budget = MoneyField(
        max_digits=14, decimal_places=2, default_currency='USD'
    )

    budget_type = models.IntegerField(choices=BUDGET_TYPE, default=0)
    project_status = models.IntegerField(choices=PROJECT_STATUS, default=0)
    project_type = models.IntegerField(choices=PROJECT_TYPE, default=0)

    created_on = models.DateTimeField(auto_now_add=True)
    project_end_date = models.DateField(blank=True, null=True)
    project_start_date = models.DateField()
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def _url(self):
        return format_html(
            '<a href="{url}" target="_blank">{url}</a>'.format(url=self.url)
        )

    def _mobile_url(self):
        return format_html(
            '<a href="{url}" target="_blank">{url}</a>'.format(
                url=self.mobile_url
            )
        )

    def _demo_video_link(self):
        return format_html(
            '<a href="{url}" target="_blank">{url}</a>'.format(
                url=self.demo_video_link
            )
        )

    def _logo(self):
        if self.logo:
            return format_html(
                '<img src="/media/{}" width="150" height="150" />'.format(
                    self.logo
                )
            )
    _logo.short_description = 'Project Logo'

    def _client_detail(self):
        base_url = "/admin/project_management/client/"
        if self.client:
            return format_html(
                '<a href="{}{}/" target="_blank">{} {}</a>'.format(
                    base_url, self.client.id, self.client.first_name,
                    self.client.last_name
                )
            )
        else:
            return u""

    def _tags(self):
        base_url = "/admin/project_management/tags/"
        return format_html(
            ' | '.join(
                ['<a href="{}{}/change/" target="_blank">{}</a>'.format(
                    base_url, tag.id, tag.name
                ) for tag in self.tags.all()]
            )
        )

    def _technologies(self):
        base_url = "/admin/project_management/technology/"
        return format_html(
            ' | '.join(
                ['<a href="{}{}/change/" target="_blank">{}</a>'.format(
                    base_url, tech.id, tech.name
                ) for tech in self.technologies.all()]
            )
        )


class List(models.Model):
    # Relations
    projects = models.ManyToManyField(Project)

    created_by = models.ForeignKey(
        User, related_name='created_lists', on_delete=models.CASCADE,
        default=1
    )
    updated_by = models.ForeignKey(
        User, related_name='updated_lists', on_delete=models.CASCADE,
        default=1
    )

    # Attributes
    name = models.CharField(max_length=250, verbose_name='List Name')

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Custom Project List"

    def __str__(self):
        return self.name

    def _projects(self):
        base_url = "/admin/project_management/project/"
        return format_html(
            ' | '.join(
                ['<a href="{}{}/" target="_blank">{}</a>'.format(
                    base_url, project.id, project.name
                ) for project in self.projects.all()]
            )
        )
