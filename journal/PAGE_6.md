# PAGE 6

## time: 28.05.2026, 17:28 EET 

## Status

Today I focused on designing the models I am going to use in order to interact with the SQLite3 database. I designed 
the following classes:
- PostgreSQLVM - this is the VM provisioned
- PostgreSQLInstance - this represents the PostgreSQL cluster
- PostgreSQLDatabase - the databases contained by the instance/cluster
- PostgreSQLBackup - this represents the backup performed by the pgBackRest - the backup is performed at 
instance/cluster level and not at the database level (for that, we will use dumps)
- PostgreSQLUser - this represents the user (role) inside the PostgreSQL database 

This is the structure I designed so far. Further updates will come.

# TO-DO

- Need to work (design) on serializers and viewsets. 
- Link the new logic (instance, backup, etc.) to the Ansible logic.
