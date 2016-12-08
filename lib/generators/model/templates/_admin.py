from django.contrib import admin
from {{appsDir}}.{{appName}}.models import {{capitalize modelName}}
{{#if order}}
from adminsortable2.admin import SortableAdminMixin
{{/if}}


class {{capitalize modelName}}Admin({{#if order}}SortableAdminMixin, {{/if}}admin.ModelAdmin):
    {{#if isPrepopulated}}
    prepopulated_fields = {"slug": ("{{prepopulated}}",)}
    {{else}}
    pass
    {{/if}}


admin.site.register({{capitalize modelName}}, {{capitalize modelName}}Admin)
