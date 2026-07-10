# PAGE 7

## time: 10.07.2026, 14:58 EET 

Today I managed to perform a full backup using exclusively an API POST request. 

What I need to do in order to fully integrate the backup logic with the Django API is to perform a PUT request after 
the backup is completed to update metrics like the timestamp, wal start/stop, database size, etc etc.  
