Django Wools
============

Django tools from WITH.

That's a collection of things that we at [WITH](https://with-madrid.com/) got
tired of copy/pasting in every project.

## Install

```
pip install django_wools
```

## Included Wools

### Storage

#### `django_wools.storage.GzipManifestStaticFilesStorage`

That's a sub-class of the 
[ManifestStaticFilesStorage](https://docs.djangoproject.com/en/3.0/ref/contrib/staticfiles/#manifeststaticfilesstorage)
but that makes sure that along with all the files comes a `.gz` version which
is easy to pick up for nginx (or other static files server).

### Middlewares

#### `django_wools.middlewares.NowMiddleware`

Suppose that you have a content that is available up until a given date. When
the date is passed then everything related to this content expires. However,
in order to do this, you're probably going to make several request, possibly in
loosely connected parts of your code. In those cases, when looking at the time,
the clock will show different value as the time passes between calls. It means
that you could very well end up with one half of your code considering that the
object is still valid but the other half that it expired.

In order to prevent this, the simplest is to consider that the time is fixed
and that the code executes instantly at the moment of the request. The goal
of this middleware is to save the current time at each request and then to
provide an easy way to get the current time through the request.

If the middleware is activated, you should be able to get the time like this:

```python
from time import sleep
from django.shortcuts import render

def my_view(request):
    print(f"Now is {request.now()}")
    sleep(42)
    print(f"Now is still {request.now()}")

    return render(request, "something.html", {"now": request.now()})
```

#### `django_wools.middlewares.SlowMiddleware`

When developing a SPA or hybrid app, you want to make sure that the app is
structurally ready to handle load times from the server, even if the connection
is a bit shaky. Also, you want to make sure that not too many requests are
sent.

In order for you to fully realize how slow your website is going to be on a bad
connection, th e SlowMiddleware will automatically add a delay before replying
to each request.

Add this to your `settings.py`

```python
MIDDLEWARE = [
    # ...
    "django_wools.middlewares.SlowMiddleware",
]

SLOW_MIDDLEWARE_LATENCY = 1 if DEBUG else 0
```

By doing this, your requests will be added a 1s delay if the `DEBUG` mode is
enabled.

### Database

#### `django_wools.db.require_lock`

Provides a way to explicitly generate a PostgreSQL lock on a table.

By example:

```python
from django.db.transaction import atomic
from django_wools.db import require_lock

from my_app.models import MyModel


@atomic
@require_lock(MyModel, 'ACCESS EXCLUSIVE')
def myview(request):
    # do stuff here
```
