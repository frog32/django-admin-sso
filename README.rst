================
Django admin SSO
================

.. image:: https://travis-ci.org/frog32/django-admin-sso.png?branch=master
    :target: https://travis-ci.org/frog32/django-admin-sso

.. image:: https://coveralls.io/repos/frog32/django-admin-sso/badge.png?branch=master
    :target: https://coveralls.io/r/frog32/django-admin-sso

.. image:: https://pypip.in/v/django-admin-sso/badge.png
    :target: https://pypi.python.org/pypi/django-admin-sso/

Django admin SSO lets users login to a django admin using an openid provider. It
then looks up the email address of the new user and looks up the rights for them.

Installation
------------

1. Make sure you have a working django project setup.
2. Install django-admin-sso using pip::

    pip install django-admin-sso

3. Add ``admin_sso`` to ``INSTALLED_APPS`` in your ``settings.py`` file::

    INSTALLED_APPS = (
        ...
        'admin_sso',
        ...
    )

4. Add the django-admin authentication backend::

    AUTHENTICATION_BACKENDS = (
        'admin_sso.auth.DjangoSSOAuthBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

5. Insert your oauth client id and secret key into your settings file::

    DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID = 'your client id here'
    DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET = 'your client secret here'

If you don't specify a client id django-admin-sso will fallback to openid.

6. Run syncdb to create the needed database tables.

7. Log into the admin and add an Assignment.


Assignments
-----------
Any Remote User -> Local User X
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Select Username mode "any".
* Set Domain to your authenticating domain.
* Select your local user from the User drop down.


Remote User -> Local User
~~~~~~~~~~~~~~~~~~~~~~~~~
* Select Username mode "matches" *or* "don't match".
* Set username to [not] match by.
* Set Domain to your authenticating domain.
* Select your local user from the User drop down.


Changelog
---------

1.0
~~~

* Add support for OAuth2.0 since google closes its OpenID endpoint https://developers.google.com/accounts/docs/OpenID
* Using OpenID is now deprecated and OpenID support will be removed in a future release.
* Add more tests to get a decent coverage.
