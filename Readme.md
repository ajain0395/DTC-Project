# System Setup
## Install Anaconda for python3
https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart
reboot
## Other Setup required
sudo sh install_all.sh
## Database setup
$ sudo - i -u postgres
$ psql -U postgres
 # CREATE USER dtc WITH PASSWORD ‘dtc’;
 # CREATE DATABASE dtcdb OWNER dtc;
 # \q
$ psql -U postgres dtcdb
 # CREATE EXTENSION postgis;

reboot
