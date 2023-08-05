# ahlev django uikit
![pypi](https://img.shields.io/pypi/v/ahlev_django_uikit) ![pypi](https://img.shields.io/pypi/status/ahlev_django_uikit)


## install from this repository
### clone

> git clone https://github.com/ohahlev/ahlev_django_uikit.git

### go to directory ahlev_django_uikit

> cd ahlev_django_uikit

### create installer package

> make package

### install package

cd into project directory

> cd ../my_project_dir

install ahlev_django_uikit from the project directory

> pip install ../ahlev_django_uikit/dist/ahlev_django_uikit-0.0.1.tar.gz


## install from pypi
[ahlev_django_uikit](https://pypi.org/project/ahlev_django_uikit/)

## project configuration
### add ahlev_django_uikit to settings.py

    INSTALLED_APPS = [
      'ahlev_django_uikit',  # add this line
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
### login
![](screenshots/login.jpg)

### dashboard
![](screenshots/dashboard.png)

### change password
![](screenshots/change-password.png)

### list users
![](screenshots/list-users.png)

