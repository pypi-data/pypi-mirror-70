==============
django-db-logs
==============

Disclaimer
----------

Update from django-db-logger, due to inactivity of the original package.

Original readme
---------------

Django logging in database.
For large projects please use `Sentry <https://github.com/getsentry/sentry>`_

Screenshot
----------
.. image:: https://ciciui.github.io/django-db-logger/static/img/django-db-logger.png

Dependency
----------
* Django>=1.9
* Python 2.7+/3.6+

License
-------
MIT

Quick start
-----------

1. Install

.. code-block:: bash

    pip install django-db-logs

2. Add "django_db_logs" to your ``INSTALLED_APPS`` setting like this

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_db_logs',
    )

3. Add handler and logger to ``LOGGING`` setting like this

.. code-block:: python

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(asctime)s %(message)s'
            },
        },
        'handlers': {
            'db_log': {
                'level': 'DEBUG',
                'class': 'django_db_logs.db_log_handler.DatabaseLogHandler'
            },
        },
        'loggers': {
            'db': {
                'handlers': ['db_log'],
                'level': 'DEBUG'
            }
        }
    }

4. Run ``python manage.py migrate`` to create django-db-logs models.
5. Use ``django-db-logs`` like this

.. code-block:: python

    import logging
    db_logs = logging.getLogger('db')

    db_logs.info('info message')
    db_logs.warning('warning message')

    try:
        1/0
    except Exception as e:
        db_logs.exception(e)



Options
-------
1. DJANGO_db_logs_ADMIN_LIST_PER_PAGE: integer. list per page in admin view. default ``10``
2. DJANGO_db_logs_ENABLE_FORMATTER: boolean. Using ``formatter`` options to format message.``True`` or ``False``, default ``False``