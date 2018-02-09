# Drupal Authentication Backend for Django

This package provides an authentication backend that can be used to facilitate migrating users from a Drupal-based website into a Django-based web application.


## Quick start

Install `django_drupal_auth_backend`:

```bash
$ pip install django_drupal_auth_backend
```

In your settings module you will need to add the new hasher to :

```python
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
    'django_drupal_auth_backend.hashers.DrupalPasswordHasher',
)
```


## Migrating users

You will need to create a user entry for each user of the old system. While this will vary from application to application (depending on whether you override the default user model provided by Django), the basic step is to copy your user table into Django's user table. If you are using Postgres, you can copy the users in with something like this:

```sql
COPY INTO auth_user (username, password, email, is_active, is_staff) FROM STDIN;
user1	drupal_sha512$FYEWxwlWtUUj8uB5QN2K0X9lNrnRl/hLpN3Qp8GK7v8emyc9eRsf	user1@example.com	t	f
user2	drupal_sha512$CsaltsaltA112iY375iFdNhp.gYEWxwlWtXdhjl.8hY7BufRTJ1u	user2@example.com	t	f
\.
```

The most important thing to note with migrated accounts is that the hashed password being migrated needs to be modified slightly. Drupal passwords are of the form:

    $S$CsaltsaltA112iY375iFdNhp.gYEWxwlWtXdhjl.8hY7BufRTJ1u

... whereas the migrated passwords need to be of the form:

    drupal_sha512$CsaltsaltA112iY375iFdNhp.gYEWxwlWtXdhjl.8hY7BufRTJ1u

The important distinction is that the `$S$` at the start of the hash needs to be converted to `drupal_sha512$` for the Django authentication backend subsystem to be able to recognize it and assign it to the `DrupalPasswordHasher`. Note that the example table copy command above is using passwords of the right form.


## Full documentation

(needs additional documentation)


## Contributing

Contributions are welcome.


## Licensing

This software is licensed under the GNU 3.0 license to comply with the Drupal license requirements for derivative works. Parts of this code are directly converted to Python from code in the Drupal project.
