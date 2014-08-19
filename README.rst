###################
Django admin lock
###################



*******
Install
*******

It is strongly recommanded to install this app from GIT with PIP onto you project virtualenv.


.. code-block::  shell-session

   pip install -e git+https://github.com/tomaszroszko/django-admin-lock.git#egg=django-admin-lock


Add app to you settings.py

.. code-block::  python

    INSTALLED_APPS = (
        ...
        'adminlock'
        ...
    )


Run syncdb and migrate command

.. code-block::  shell-session

    python manage.py syncdb
    python manage.py migrate


*******
Usage
*******

Edit admin.py file in your app

.. code-block::  python

    from django.contrib import admin
    from adminlock.admin import AdminLock

    from .models import YourModel


    class YourModelAdmin(AdminLock):
       pass


    admin.site.register(YourModel, YourModelAdmin)
