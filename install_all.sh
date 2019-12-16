sudo apt install build-essential ubuntu-restricted-extras
sudo apt install postgis
sudo apt-get install curl ca-certificates gnupg
curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo touch /etc/apt/sources.list.d/pgdg.list
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ (lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
sudo apt-get update
sudo apt-get install postgresql-11 pgadmin4 postgis
pip install -r requirements.txt
