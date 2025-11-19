- First I logged into GCP and created a new vm instance called **assignment4-504**. 
    - Location: `us-central1-f` 
- I created a firewall rule to allow access to port 22 and 3306. 
- I then opened the `SSH` for my vm and ran: `sudo apt-get update` and `sudo apt install mysql-server mysql-client -y`  to install MySQL 
- I created a folder structure: **myproject/scripts/**
    - I created vm_demo.py inside scripts/.
- I created `.env `file and stored MySQL credentials and database info securely. 
- I then had to exit out of the SSH and reopen it to run `sudo mysql` so I could log in. 
- I then created a new user called **dba** and granted it all privileges with the following command: `GRANT ALL PRIVILEGES ON *.* TO 'dba'@'%' WITH GRANT OPTION` 
- I then created a new database called **dummydba** using the command `create database dummydba` 
- I then ran `sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf` to change the binding address to `0.0.0.0` 
- I then ran the following command: `sudo systemctl daemon-reload` and `sudo systemctl start mysql` 
- I used the command `nano vm_demo.py` to copy paste my script from the vs code file: `vm_demo.py`. 
- I then did `python3 vm_demo.py`
- I ran the command: `mysql -u dba -p` and entered my password. I was able to connect and ran the following:
    - `USE dummydba` 
    - `show tables`
    - `select * from visits` to see my table 

I had trouble with the running my code in the SSH due to the "?ssl=false". I had to delete that to get my script to run. Additionally, I had to disconnect from my SSH multple times to run `sudo` commands. This was frustrating. 