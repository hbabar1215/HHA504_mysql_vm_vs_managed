# Creating the Managed DB on GCP 
- To create a managed db I logged into GCP and selected **Cloud SQL** 
    - Cloud SQL edition: Enterprise 
    - Database version: MySQL 8.4
    - Instance ID: assignment4-504
    - Region: us-central1 (Iowa) and single zone
    - 1 vCPU, 3.75 GB
    - Storage: 10GB
    - Instance IP assignment: Public
        - Authorized networks: Allow `0.0.0.0/0`
    - Security: Allow unencrypted network traffic 
- After creating the db called assignment4-504 it took 5 minutes for the instance to load. 

User Creation 
- I then created a user db504 and opened up Google cloud shell to connect to mysql:
`mysql -u db504 -h 35.224.240.90 -p`
- I tried to grant user db504 permission with the command `GRANT ALL PRIVILEGES on *.* TO 'db504'@'%' WITH GRANT OPTION` however this did not work. I constantly received the following error: ERROR 1045 (28000): Access denied for user 'db504'@'%' (using password: NO)
- To troubleshoot, I created a password for this user (db504) and ran the permission command again, however this did not work. 
- I then created the `init.sql` file which helped me run my code by creating the visits in my database. 


