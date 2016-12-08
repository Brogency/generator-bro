# Generators

Package contain next generators:

## App

Main generator for creating django project file structure. Generator create
project file structure, create file with dependencies, create stub for local
settings and complete file with you local settings such as database driver,
name, user and password data.

**Command**

```bash
$ yo bro <projectName> [options]
```

**Example:**

```bash
$ yo bro my_project
```

After this command will been complete, you get next file structure:

```
my_project
├── docker-compose.override.yml
├── docker-compose.production.yml
├── docker-compose.yml
├── fabfile.py
├── readme.md
└── server
    ├── apps
    │   └── __init__.py
    ├── config
    │   ├── celery.py
    │   ├── dashboard.py
    │   ├── __init__.py
    │   ├── settings
    │   │   ├── celery.py
    │   │   ├── constance.py
    │   │   ├── dbmail.py
    │   │   ├── grappelli.py
    │   │   ├── __init__.py
    │   │   ├── installed_apps.py
    │   │   ├── locale.py
    │   │   └── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── docker-compose.test.yml
    ├── dockerfile
    ├── fabfile.py
    ├── manage.py
    ├── requirements.txt
    └── static

```

Description for this structure: |
----  | -----------
.yo-rc.json| Configure file for generator, do not remove this.
client| Directory for your static files such as css, js, images and others.
server| Directory for your django project.
server/apps | Python package for your django apps.
server/libs | Directory for your python libraries.
server/contrib | Directory for application that you fork and will be support.
server/config | This package contain that what you see.
server/config/settings | This package contain your project settings.
server/config/settings/installed_apps.py | File contain tuple with your apps. Sub generator will update this file and append to it new apps names.
server/config/urls.py | File contain root url conf for your apps. Sub generator will update this file and include to it new urlpatterns.

# TODO not actual now

!!! danger "Do not remove file .yo-rc.json"
    If you remove this file then others sub generators will not work for you project.
```

## Sub

Generator for creating django application. This generator create file structure
for your app in directory with your other apps. Include this application to your
settings file and include urls patterns for this app to root url conf.

**Command**

```bash
$ yo bro:sub <appName> [options]
```

**Options**

**--force** overwrite files which already exist.

**Example:**

```bash
$ yo bro:sub news
```

After completion of commands, will create the following files:

```python
news
├─ models
|  ├─ mixins
|  |  └─ __init__.py
|  └─ __init__.py
├─ views
|  ├─ mixins
|  |  └─ __init__.py
|  └─ __init__.py
├─ factories
|  └─ __init__.py
├─ admin
|  ├─ mixins
|  |  └─ __init__.py
|  └─ __init__.py
├─ tests
|  ├─ models
|  |  └─ __init__.py
|  ├─ views
|  |  └─ __init__.py
|  └─ __init__.py
├─ urls.py
└─ __init__.py
```

Next files will be update:|
----- | ------
server/config/settings/installed_apps.py|To this file will be append string with name for new app.
server/config/urls.py|To this file will be include urlpatterns from new app **server/apps/news/urls.py**.

## Model

Generator for creating django models. Create models for application and register
this in admin panel. This is very easy way for creating your models. Your can
create model with fields which you want from console usage short name for django
fields types. For run generator enter command like in example to below.

**Command**

```bash
$ yo bro:model <appName>:<ModelName> [<fieldName>:<shortName>[:<arg1,arg2=value>] ...] [options]
```

**Arguments**

Description|
-----|-----
appName| is name of you application
ModelName| is name for your new model. Must be in **UpperCamelCase**.
Fields| next arguments is optionality. If you do not enter their, model will be create without model fields.
fieldName| is name for your field. Name fields must be in **snake_case** ([PEP8](https://www.python.org/dev/peps/pep-0008/)).
shortName| is short name for type of model fields (see list with short names [below](#shortnames)).
Arguments| for every field is not required. Args must be separated by commas. This arguments will be include to model field initialize.

**Options**

**-s**, **--def-save** create model method save for new model.

**-f**, **--force** overwrite files that already exist.

**-p**, **--prepopulated** prepopulated field name for admin class.

**--model** file name when you want create model (set filename only without extension).

**--admin** file name when you want create admin class for model (set filename only without extension).

**-o**, **--order** create field order, and add class Meta: ordering=('order', )

**Example:**

```bash
$ yo bro:model news:News title:char content:text hidden:bool:default=False created:datetime
```

This command create next code:

```python
class News(models.Model):
    title = models.CharField(
        max_length=255
    )
    content = models.TextField(
        
    )
    hidden = models.CharField(
        default=False
    )
    created = models.DateTimeField(
        
    )

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
```

<a name="shortnames"></a> Full list of short names for model fields

Short name | Model field | Default value
-----------|-------------|--------------
auto       | AutoField   |
bigInteger | BigIntegerField|
binary     | BinaryField |
bool       | BooleanField|
char       | CharField   | max_length=255
commaSepInt| CommaSeparatedIntegerField | max_length=255
date       | DateField   |
dateTime   | DateTimeField|
decimal    | DecimalField|
email      | EmailField  |
file       | FileField   |
filePath   | FilePathField|
float      | FloatField  |
image      | ImageField  |
int        | IntegerField|
ip         | IPAddressField|
genericIp  | GenericIPAddressField|
nullBool   | NullBooleanField|
positiveInt| PositiveIntegerField|
positiveSmallInt| PositiveSmallIntegerField|
slug       | SlugField   |
smallInt   | SmallIntegerField|
text       | TextField   |
time       | TimeField   |
url        | URLField    |
fk         | ForeignKey  |
m2m        | ManyToManyField|
o2o        | OneToOneField|
redactor   | Redactor    |

## View

Generator for creating generic views. With help this generator you can very fast
create views for your model. Just enter your model name and tell what kind of views
you want and generator create them for you.

**Example:**

```bash
$ yo bro:view news:News --list
```

This command create next code:

```python
class NewsListView(ListView):
    model = News
    paginate_by = 5

    def get_queryset(self):
        """Override this method or remove."""
        return super(NewsListView, self).get_queryset()

    def get_context_data(self, **kwargs):
        """Override this method or remove."""
        context = super(NewsListView, self).get_context_data(**kwargs)
        context.update({})
        return context
```

Also generator create urlpatterns and base templates for your views. After
generator complete your works you can run django server and check that views works.

With generator you can create next generic views:

### ListView

For create this view run command with option `--list`. With this option you can
set option `--paginate` this option given integer number and setting for views
count items per page, by default value is 5.

For this view will be created **template: model_name_list.html**

### DetailView

For create this view run command with option `--detail`.

For this view will be created **template: model_name_detail.html**

### CreateView

For create this view run command with option `--create`. For create view and
update view will be created empty model form class **ModelNameForm**.

For this view will be created **template: model_name_form.html**

### UpdateView

For create this view run command with option `--update`.

For this view will be created **template: model_name_form.html**

### DeleteView

For create this view run command with option `--del`.

## Serializer

Create **DRF** serializer for your model.

**Example:**

```bash
$ yo bro:serializer news.News
```

This command create file news.py in serializers package:

```python
from apps.news.models.news import News
from rest_framework import serializers


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
```

*If serializers package does not exists, will be create.*

You can use option **--file** for writing serializer to some existing file.

**Example:**

```bash
$ yo bro:serializer news.News --file=path/to/file.py
```

Option file take path to destination file relatively app directory **news**.

To file **apps/news/path/to/file.py** will be writing next code:

```python
...

from apps.news.models.news import News
from rest_framework import serializers

...

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
```

## Viewset

Create **DRF** viewset for your model.

**Example:**

```bash
$ yo bro:viewset news.News
```

This command create file news.py in viewsets package and update urls.py for **news** app:

```python
from apps.news.viewsets.news import NewsSerializer
from apps.news.models.news import News
from rest_framework import viewsets


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
```

*If viewsets package does not exists, will be create.*

To urls.py will be add next string:

```python
router.register('news', NewsViewSet)
```

Viewset command also support **--file** option like a serializer (see above).

## Config

If you want use generator-bro with your project which already exists and was created without generator.
You need use sub generator **bro:config**. This generator create config file **.yo-rc.json**
and other settings files for your django project that provide work for other sub generators (see above).

**Example:**

Go to your project dir.

```bash
$ cd /path/to/your/project
```

And run next command from your project root directory.

```bash
$ yo bro:config
```

You can run command with options or without. If you run command without options
you will need to answer a few questions in interactive mode.

**List options**

**--settings** path to django project settings dir. If you not use settings package and
use a single settings file you need create settings package.

**--apps** path to your apps directory.

**--urls** path to your root urls conf file.

**--templates** path to your templates directory this options **is not required**

!!! note "Relative path"
    All paths should be relatively of your project. For example if path for your
    project **/path/to/your/project** and path to your apps **/path/to/your/project/my_apps**
    then set option apps like this **--apps my_apps**