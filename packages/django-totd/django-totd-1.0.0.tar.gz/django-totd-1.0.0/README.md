# Tip of the Day (totd)

A Django application that allows you to create tips or hints to be displayed at the top of specific pages on your website. This app allows you to define tips in the Django Admin, assign them to specific pages, and give a date range in which they should be displayed.

# Installation

Install the Django Tip of the Day package:

`pip install django-totd`

# Settings

Add `totd` to your INSTALLED_APPS:

```
INSTALLED_APPS = [
    ...
    "totd",
]
```

Add the `tips` Context Processor:

```
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                ...
                "totd.context_processors.tips",
            ]
        },
    }
]
```

# Templates

Totd works a lot like the Django Messages framework, you should add it to the top of the content portion of your base template so that it can be used in any page extending that template. The URL path of the request will be used to decide which Tip to show.

Add the following snippet to your base template:
```
{% if tip %}
<div class="alerts">
    <div class="alert {{ tip.tags }}"><strong>{% trans "Tip:" %}" </strong>{{ tip.text|safe }}</div>
</div>
{% endif %}
```