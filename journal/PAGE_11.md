# PAGE 11

## time: 28.07.2026, 15:34 EET 

To enter the Django shell, use: 

```python
python manage.py shell
```

Once you opened the shell, paste the following to check the ClockedSchedule, IntervalSchedule and CrontabSchedule 
instances and delete them: 

```commandline
from django_celery_beat.models import (
    PeriodicTask,
    ClockedSchedule,
    IntervalSchedule,
    CrontabSchedule,
)

ClockedSchedule.objects.all()
IntervalSchedule.objects.all()
CrontabSchedule.objects.all()

ClockedSchedule.objects.all().delete()
IntervalSchedule.objects.all().delete()
CrontabSchedule.objects.all().delete()

```
