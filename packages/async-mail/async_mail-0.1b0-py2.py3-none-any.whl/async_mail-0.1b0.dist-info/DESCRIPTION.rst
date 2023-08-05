==========
async_mail
==========


.. image:: https://img.shields.io/pypi/v/async_mail.svg
        :target: https://pypi.python.org/pypi/async_mail

.. image:: https://img.shields.io/travis/larsclaussen/async_mail.svg
        :target: https://travis-ci.com/larsclaussen/async_mail

.. image:: https://readthedocs.org/projects/async-mail/badge/?version=latest
        :target: https://async-mail.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


By django inspired async mail package.

Supports simple-settings and django settings. These settings entries are expected
to be present ::

    EMAIL_BACKEND = 'async_mail.backends.smtp.EmailBackend'
    EMAIL_SENDER = 'no-reply@nelen-schuurmans.nl'
    EMAIL_HOST = 'your-host-name'

    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_PORT = 25
    EMAIL_USE_TLS = True
    EMAIL_TIMEOUT = 5



Example
-------

To send a single mail ::

    from async_mail import Mail
    from async_mail.models import Message

    mail = Mail()
    message = Message(
        sender="lars.claussen@mail.com",
        recipients=["lars.claussen@mail.com"],
        subject="one mail",
        message_body="one mail to rule them all"
    )
    await mail.send_message(message)


TODO
--------

* console backend
* pydantic settings support
* multiple SMTP clients instead of gather for true async execution


* Free software: MIT license
* Documentation: https://async-mail.readthedocs.io.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


=======
History
=======

0.1b (2020-06-03)
-----------------

- Beta release.




