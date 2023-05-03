sudo apt update
sudo apt install python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl


cd /home/ubuntu 
git clone

python3 -m venv .venv


cd 

sudo cp deploy/gunicorn/gunicorn.socket  /etc/systemd/system/gunicorn.socket

sudo cp deploy/gunicorn/gunicorn.service /etc/systemd/system/gunicorn.service

sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket


## Nginx

sudo apt install nginx

sudo /home/ubuntu

sudo cp deploy/nginx/softether /etc/nginx/sites-available/softether

sudo ln -s /etc/nginx/sites-available/softether /etc/nginx/sites-enabled
