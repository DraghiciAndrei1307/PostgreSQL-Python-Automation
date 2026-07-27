# PAGE 9

## time: 23.07.2026, 10:17 EET 

Today marks an important milestone achieved. Today I managed to fully integrate the Celery Beat scheduler into my 
architecture and perform a scheduled full backup. I will describe the process down below. 

Everything started with this article: 
[A Complete Guide to Configuring Celery & Celery Beat on a Ubuntu Server](
https://medium.com/@arun.arunisto2/a-complete-guide-to-configuring-celery-celery-beat-on-a-ubuntu-server-django-redis-systemd-6f3067d683aa)

As the title mentions, this article helps you integrate the Celery & Celery Beat into you Django project. 

As you may probably know already, I am not using Ubuntu to create my VMs. I am using RedHat/Rocky Linux. So these steps
were adjusted for these distros.

These are the steps performed:

1) Install the celery (for redis) inside your venv

```commandline
pip install "celery[redis]"
```

2) Install & Enable Redis on Linux Server

```commandline
dnf install -y redis
systemctl enable --now redis
```

3) Inside the Django project configuration folder, create a file named `celery.py`.

MENTION: Check the following path in this repo: [django_rest_api/django_api/celery.py](
../django_rest_api/django_api/celery.py)

The `django_api` represents our Django project. In this folder we should pretty much put all the configuration files,
like celery.py.

The `celery.py` contains the following: 

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_api.settings')

app = Celery('django_api')
app.conf.enable_utc = False

app.config_from_object("django.conf:settings", namespace='CELERY')

app.autodiscover_tasks()
```

In this file:
- we are configuring the `DJANGO_SETTINGS_MODULE` env variable to point to the `settings.py` file
inside the django_api folder (check [`settings.py`](../django_rest_api/django_api/settings.py))

- we are creating the Celery app and configure this app using the [`settings.py`](
../django_rest_api/django_api/settings.py) file where we defined some special Celery parameters we will discuss down below.

- we set the `autodiscover_tasks()` so that Celery can auto-discover tasks that were created and need to be executed by 
the worker (this pretty much makes it possible for celery to detect the tasks we defined in 
[`provisioner_api/tasks.py`](../django_rest_api/provisioner_api/tasks.py); we will discuss this later)

4) Inside [`__init__.py`](../django_rest_api/django_api/__init__.py), we are:

- importing the `app` object from `celery.py`
- give it an alias `celery_app`
- makes it available when someone imports the package
- `__all__` mentions which names are exported when someone does `from django_api import *`; also, the `celery_app` 
object is already exposed outside the package because we imported it into the `__init__.py` 

```python
from .celery import app as celery_app

__all__ = ("celery_app",)
```

5) On the Linux server, create the `/etc/default/celery`. 

This is the environment configuration of Celery.

Inside this file, create the following: 

```bash
CELERY_APP=django_api
CELERY_BIN=/home/student/venvs/venv/bin/celery
CELERY_POOL=threads
CELERY_CONCURRENCY=16
CELERY_LOG_LEVEL=INFO
```

The following env variables were created: 
- `CELERY_APP`: The name of the project
- `CELERY_BIN`: This is the path to the `Celery executable`. The Celery executable was created when we installed Celery 
inside our Python venv with this command `pip install "celery[redis]"`
- `CELERY_POOL`: The celery worker will create threads instead of processes. 
- `CELERY_CONCURRENCY`: this option mentions how many tasks can be executed simultaneously. In our case, one worker can 
perform 16 tasks in parallel. 
- `CELERY_LOG_LEVEL`: Sets the minimal level of severity of the log messages

This is the table of log levels:

| Level    | Meaning                                                           | 
|----------|-------------------------------------------------------------------|
| `DEBUG`    | Detailed info, used for debugging.                                |
| `INFO`     | Normal events(worker start, received tasks, finished tasks, etc.) |
| `WARNING`  | Unusual situations which do not stop the app.                     |
| `ERROR`    | Errors which stopped the execution of a task/operation.           |
| `CRITICAL` | Critical errors which can disturb the worker functionality.       |

6) Create startup scripts

The article says that we should never run Celery directly from systemd. Instead, we should use predefined scripts.

So, I created the following scripts for `Celery` and `Celery Beat`: 

- `/usr/local/bin/run_celery.sh` which contains:

```bash
#!/bin/bash
source /etc/default/celery
source /home/student/venvs/venv/bin/activate
exec $CELERY_BIN -A $CELERY_APP worker --pool=$CELERY_POOL --concurrency=$CELERY_CONCURRENCY -l $CELERY_LOG_LEVEL
```

- `/usr/local/bin/run_celerybeat.sh` which contains:

```bash
#!/bin/bash
source /etc/default/celery
source /home/student/venvs/venv/bin/activate
exec $CELERY_BIN -A $CELERY_APP beat -l $CELERY_LOG_LEVEL --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

Also, we need to make sure these files are executable:
```commandline
sudo chmod +x /usr/local/bin/run_celery.sh
sudo chmod +x /usr/local/bin/run_celerybeat.sh
```

7) We will now create the 2 systemd services for Celery and Celery Beat

    7.1) Create the `/etc/systemd/system/celery.service` service unit file:

    ```commandline
    touch /etc/systemd/system/celery.service
    ```

    7.2)    Paste the following inside the file:

    ```bash
    [Unit]
    Description=Celery Worker Service
    After=network.target redis.service
    
    [Service]
    User=student
    Group=student
    WorkingDirectory=/home/student
    EnvironmentFile=/etc/default/celery
    Environment="DJANGO_SETTINGS_MODULE=django_api.settings"
    ExecStart=/usr/local/bin/run_celery.sh
    Restart=always
    RestartSec=5
    
    [Install]
    WantedBy=multi-user.target
    ```
    
    I will try to explain down below what these thing are meaning.
    
    The `After` directive mentions the startup ordering. In our service file, we mention that we want this unit to be 
    started right after the `network.target` and `redis.service` units. 
    
    Inside the `[Service]` section describes the way the service is executed. We mention the privileges the Celery will be 
    executed as (`User` and `Group` directives). 
    
    The `WorkingDirectory` directive sets the working directory before the startup of the service. This is the current directory from
    which the script mentioned in `ExecStart` directive (in our case `/usr/local/bin/run_celery.sh`) is executed.
    
    The `EnvironmentFile` directive is the path to the file where we declared the Celery worker env variables. 
    
    The `Environment` directive lets us create a env variable. In our case we create `DJANGO_SETTINGS_MODULE` which tells 
    Django to use the `django_api.settings` module for configuration.
    
    The `Restart` directive is set to restart. This means if the Celery process is stopped, it will be restarted \
    automatically by systemd. 
    
    The `RestartSec` is set to `5`. This means the systemd will wait for 5 minutes before starting the Celery service. 
    
    The `WantedBy` directive creates a symbolic link to the `multi-user.target` unit. This means that the celery.service 
    will be started automatically when the system reaches the normal functioning state (described inside the 
    `multi-user.target` unit) 
    
    The flux described in the `celery.service` service unit file is:

    - The system reaches the `multi-user.target` (normal functioning state)
    - If the service is enabled `systemctl enable celery`, which normally should be, then the `systemd` will try to 
    start the `celery.service` service unit
    - Then, it waits for `network.target` and `redis.service` to be started, as it is mentioned in the `After=` 
    directive
    - It tries to load the env variables from `/etc/default/celery` and defines the `DJANGO_SETTINGS_MODULE`
    - Switches the user to `student`
    - Sets the working directory to `/home/student`
    - Runs the script `/usr/local/bin/run_celery.sh`
    - If the worker stops, `systemd` will wait 5 seconds and will restart the `celery.service` because of the `Restart`
    directive

    7.3) Create the unit service file for the Celery Beat service
    
    ```bash 
    touch /etc/systemd/system/celerybeat.service
    ```
    7.4) Paste the following inside the service file:
  
    ```bash
    [Unit]
    Description=Celery Beat Scheduler
    After=network.target
    
    [Service]
    User=student
    Group=student
    WorkingDirectory=/home/student
    EnvironmentFile=/etc/default/celery
    Environment="DJANGO_SETTINGS_MODULE=django_api.settings"
    ExecStart=/usr/local/bin/run_celerybeat.sh
    Restart=always
    RestartSec=5
    
    [Install]
    WantedBy=multi-user.target

    ```  
   
8) Enable and Start Services

```commandline
sudo systemctl daemon-reload
sudo systemctl enable celery
sudo systemctl enable celerybeat
sudo systemctl start celery
sudo systemctl start celerybeat
```

9) Verify

```commandline
journalctl -u celery -f

journalctl -u celerybeat -f

((venv) ) [student@master-celery-redis ~]$ celery -A django_api inspect registered
->  celery@master-celery-redis: OK
    * provisioner_api.tasks.perform_backup
    * provisioner_api.tasks.run_ansible_provisioning_task

((venv) ) [student@master-celery-redis ~]$ celery -A django_api status
->  celery@master-celery-redis: OK

1 node online.

```

10) Add the following Celery configs into the `settings.py`

```commandline
CELERY_BROKER_URL = "redis://localhost:6379/0"

CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

CELERY_BEAT_SCHEDULER = (
    "django_celery_beat.schedulers:DatabaseScheduler"
)
```

11) Define the tasks inside the `django_rest_api/provisioner_api/tasks.py`

The tasks defined here should have the following decorator `@shared_task`. Also, do not forget to import it 
`from celery import shared_task`.

12) Put the `"django_celery_beat"` inside the `INSTALLED_APPS` list inside the `settings.py` module.

13) Run the following command `python manage.py migrate` or `python manage.py migrate django_celery_beat`

14) The Django migration system will create tables like:

```commandline
django_celery_beat_periodictask
django_celery_beat_intervalschedule
django_celery_beat_crontabschedule
django_celery_beat_solarschedule
django_celery_beat_clockedschedule
django_celery_beat_periodictasks
```

Now, one last thing that I want to mention here is the way that I integrated Celery and Celery Beat with the Django API 
solution. I want to explain the logic of a normal flux.

a) The first step is when a `POST` request is created to perform a full backup. In the POST body we can mention 
the time when the backup should be performed by using the `execute_at` option. 
b) Next, if the `execute_at` option was used, we create an instance of the [`BackupSchdeuler`](
../django_rest_api/provisioner_api/backup_scheduler.py) class and use the `schedule` method to create a `PeriodicTask` 
(using `django_celery_beat` module) which is configured to use the `perform_backup` task defined in `tasks.py`
c) Now, the `PeriodicTask` is saved inside the `SQLite` database (you need to execute `python manage.py migrate`) 
and is ready to be executed at the right time.
d) The `DatabaseScheduler` we set up inside the `/usr/local/bin/run_celerybeat.sh` and also inside the `settings.py` 
will read the `SQLite` table named `django_celery_beat_periodictask` and check when is the time to execute the 
PeriodicTask.
e) If the `DatabaseScheduler` decides that now is the moment to execute the task, it will send the task to `Redis` 
f) The `Celery` worker will take the task from `Redis` and execute it.

Observation: I set up the scheduler inside the `/usr/local/bin/run_celerybeat.sh` because when running the 
`Celery Beat` as a `systemd` service, it might not set up the `django_celery_beat.schedulers.DatabaseScheduler` but 
another scheduler named `celery.beat.PersistentScheduler` which I do not know why but it cannot detect the 
`PeriodicTask`s created.  

# also add here the debugging commands used and maybe talk about the IntervalSchedule after implementatiom

# I need to create a test standard to test the scheduler
