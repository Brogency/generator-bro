from django.db import models
from redactor.fields import RedactorField


class {{capitalize modelName}}(models.Model):
    {{#each fields}}
    {{{this}}}
    {{else}}
    # your database fields
    {{/each}}

    {{#if order}}
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False
    )

    {{/if}}
    class Meta:
        {{#if order}}
        ordering = ('order', )
        {{/if}}
        verbose_name = ''
        verbose_name_plural = ''
    {{#defSave}}

    def save(self, force_insert=False,
             force_update=False, using=None, update_fields=None):
        """Override this method"""
        super({{capitalize modelName}}, self).save(
            force_insert, force_update, using, update_fields)
    {{/defSave}}