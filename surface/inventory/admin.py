from . import models
from django.contrib import admin
from django.contrib.admin.decorators import register
from django.urls import reverse
from django.utils.html import format_html

from . import models


@register(models.Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_content_source', 'description', 'actions', 'enabled')
    list_filter = (
        ('content_source', admin.RelatedOnlyFieldListFilter),
        'enabled',
    )
    exclude = ('content_source',)

    def get_readonly_fields(self, request, obj=None):
        l = list(super().get_readonly_fields(request, obj=obj))
        l.insert(1, 'get_content_source')
        return l

    def get_content_source(self, obj):
        meta = obj.content_source.model_class()._meta
        return format_html(
            '<a href="{}">{}</a>',
            reverse(f'admin:{meta.app_label}_{meta.model_name}_change', args=(obj.pk,)),
            f'{meta.app_label}: {meta.verbose_name}',
        )

    get_content_source.short_description = 'Content Source'
    get_content_source.admin_order_field = 'content_source'

    def _actions(self, obj):
        return ', '.join(obj.actions)

    _actions.short_description = 'Actions'


@register(models.Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    empty for now
    """
