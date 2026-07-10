# PAGE 7

## time: 10.07.2026, 14:58 EET 

Today I managed to perform a full backup using exclusively an API POST request. 

What I need to do in order to fully integrate the backup logic with the Django API is to perform a PUT request after 
the backup is completed to update metrics like the timestamp, wal start/stop, database size, etc etc.  

## Next steps: 

- finish the backup workflow (the update after the backup is completed)
- add Flower for monitoring
- add Celery Beat to schedule the backups
- change the broker into RabbitMQ
- create a script that resets the master node...

