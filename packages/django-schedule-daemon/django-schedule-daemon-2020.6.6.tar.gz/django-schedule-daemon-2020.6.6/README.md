<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/v/django-schedule-daemon.svg?maxAge=3600)](https://pypi.org/project/django-schedule-daemon/)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)
[![Travis](https://api.travis-ci.org/andrewp-as-is/django-schedule-daemon.py.svg?branch=master)](https://travis-ci.org/andrewp-as-is/django-schedule-daemon.py/)

#### Installation
```bash
$ [sudo] pip install django-schedule-daemon
```

##### `.env`
```bash
DJANGO_SCHEDULE_MODULE=schedule_jobs
```

##### `settings.py`
```python
INSTALLED_APPS+= ['django_schedule_daemon']
```

#### Examples
`schedule_jobs.py`
```python
import schedule

from django.core.management import call_command

schedule.every(5).seconds.do(lambda:call_command('test_command'))
```

```bash
python manage.py schedule_daemon
```

#### Links
+   [schedule](https://github.com/dbader/schedule)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>