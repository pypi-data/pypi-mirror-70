# Layout Application
![pypi](https://img.shields.io/pypi/v/ahlev_django_layout) ![pypi](https://img.shields.io/pypi/status/ahlev_django_layout)

## install from this repository
### clone

> git clone https://github.com/ohahlev/ahlev_django_layout.git

### go to directory ahlev_django_layout

> cd ahlev_django_layout

### create installer package

> make package

### install package

cd into project directory

> cd ../my_project_dir

install ahlev_django_layout from the project directory

> pip install ../ahlev_django_layout/dist/ahlev_django_layout-0.0.1.tar.gz

## install from pypi
[ahlev_django_layout](https://pypi.org/project/ahlev_django_layout/)

## project configuration
### add tmp app to settings.py

    INSTALLED_APPS = [
      'ahlev_django_layout',  # add this line
      ...
    ]


### make sure these lines exist in settings.py

    STATICFILES_DIRS = [
      os.path.join(BASE_DIR, "static")
    ]
    STATIC_URL = '/static/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
    MEDIA_URL = '/medias/'

### make sure these lines exists in urls.py

    # replace tmp with application name
    from django.conf import settings
    from django.conf.urls.static import static
    from django.urls import include, path

    urlpatterns = [
       path('admin/', admin.site.urls),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

## screenshots
