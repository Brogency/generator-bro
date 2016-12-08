from rest_framework import serializers
from {{pyApp}}.models.{{cameltosnack modelName}} import {{modelName}}


class {{modelName}}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {{modelName}}