huscy.projects
======

![alt](https://img.shields.io/pypi/v/huscy-projects.svg)
![alt](https://img.shields.io/pypi/pyversions/huscy-projects.svg)



Requirements
------

- Python 3.6+
- A supported version of Django

Tox tests on Django versions 2.0, 2.1, 2.2 and 3.0.



Installation
------

To install `husy.projects` simply run:
```
pip install huscy.projects
```


Configuration
------

We need to hook `huscy.projects` into our project.

1. Add `huscy.projects` into your `INSTALLED_APPS` at settings module:

```python
INSTALLED_APPS = (
	...
	'django_filters',
	'rest_framework',

	'huscy.projects',
)
```

2. Create `huscy.projects` database tables by running:

```
python manage.py migrate
```


Development
------

After checking out the repository you should run

```
make install
```

to install all development and test requirements and

```
make migrate
```

to create the database tables.
We assume you have a running postgres database with a user `huscy` and a database also called `huscy`.
You can easily create them by running

```
sudo -u postgres createuser -d huscy
sudo -u postgres psql -c "ALTER USER huscy WITH PASSWORD '123'"
sudo -u postgres createdb huscy
```
