from django.forms import ModelForm
from {{modelPythonPath}} import {{modelName}}


class {{modelName}}Form(ModelForm):
    class Meta:
        model = {{modelName}}
        fields = '__all__'
