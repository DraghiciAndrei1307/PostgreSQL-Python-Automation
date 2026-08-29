# PAGE 12

## time: 29.08.2026, 21:21 EET 

It's been some time since I pause the development of this project. 

I am planning to create a robust MVP until the end of this month. This is the plan for the next period:

0) We need to create an ORDER model where we mention the action we need to perform (provision, perform backup, perform restore, perform delete) 
1.1) Create INF VMs -> This will be created directly on the Vagrant stage. The same time when you create the slave VM. 
		  -> We need to copy the SSH key from the SLAVE to INFs and update the VM model with some references to the INFs (which are also SLAVE VMs, but with a different type)
1.2) Rsync the backup to the INFs -> copy the backup files from SLAVE to INFs
2) Perform restore -> We will copy the backup from INF 1 to SLAVE.
	           -> Perform the actual restore.  
3) Perform delete 


For step 0:
 - We need to create a model named Order which will have a attribute named action. Depending on the action, we will have to complete some additional fields.  
 - After the order was performed, we need to perform a PATCH to update the order status (Finished/Failed).

For step 1:
 - Create an INF VM model in Django. This model will have an attribute where we will store a list with the backups contained by the INF VM
 - Use Vagrant to create some small INF vms for each SLAVE VM
 - COPY SSH FROM SLAVE to INF and also from INF to SLAVE
 - Perform full backup (need to research if I can have a 2 entries retention for a Django model)
 - PATCH req to update the backup entry
 - Copy/rsync the full backup from SLAVE to INFs 
 - PATCH req to update the INF VM entry
 - PATCH req to update the ORDER entry

For step 2: 
 - Copy/rsync the backup from INF 1 to SLAVE
 - PATCH req to update the ORDER entry status

For step 3:
 - Stop PostgreSQL instance
 - Stop SLAVE VM and and INF VMs
 - Delete the 3 VMs
 - DELETE the VMs entries and backup entries from the DJANGO database  

I also tried to create some diagrams with the flows of the things described above: 
[MVP_Plan](../docs/diagrams/MVP_Plan.png)
