from rest_framework import serializers
from {{pyApp}}.models.{{lower modelName}} import {{modelName}}


class {{modelName}}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {{modelName}}