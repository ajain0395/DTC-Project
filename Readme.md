# System Setup
## Install Anaconda for python3
https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart<br /> 
reboot
## Other Setup required
sudo sh install_all.sh
## Database setup
$ sudo - i -u postgres <br /> 

$ psql -U postgres<br /> 

\# CREATE USER dtc WITH PASSWORD ‘dtc’;<br /> 

\# CREATE DATABASE dtcdb OWNER dtc;<br /> 

\# \q<br /> 

$ psql -U postgres dtcdb<br /> 

\# CREATE EXTENSION postgis;<br /> 


reboot<br /> 
