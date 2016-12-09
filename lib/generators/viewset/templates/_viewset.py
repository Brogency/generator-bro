from rest_framework import viewsets
from {{pyApp}}.models import {{modelName}}
from {{pyApp}}.serializers import {{modelName}}Serializer


class {{modelName}}ViewSet(viewsets.ModelViewSet):
    serializer_class = {{modelName}}Serializer
    queryset = {{modelName}}.objects.all()
