from django.contrib import admin
from apps.{{appName}}.models import {{capitalize modelName}}


class {{capitalize modelName}}Admin(admin.ModelAdmin):
    {{#if isPrepopulated}}
    prepopulated_fields = {"slug": ("{{prepopulated}}",)}
    {{else}}
    pass
    {{/if}}


admin.site.register({{capitalize modelName}}, {{capitalize modelName}}Admin)
