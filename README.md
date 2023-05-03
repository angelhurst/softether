# Instalar Dependencias

```bash
sudo apt update
sudo apt install python3-venv python3-dev libpq-dev nginx curl
```

# Clonar repositorio 
git clone https://github.com/angelhurst/softether.git

```bash
cd sofsoftether

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

# Gunicorn

```bash
sudo cp deploy/gunicorn/gunicorn.socket  /etc/systemd/system/gunicorn.socket

sudo cp deploy/gunicorn/gunicorn.service /etc/systemd/system/gunicorn.service

sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
```



## Nginx

se debe modificar deploy/nginx/softether por el dominio o ip que escuchara

```bash
listen 80;
    server_name Dominio_o_IP;
```

```bash
#   copiar configuracion
sudo cp deploy/nginx/softether /etc/nginx/sites-available/softether

# crear enlaze simbolico
sudo ln -s /etc/nginx/sites-available/softether /etc/nginx/sites-enabled

# testear configuracion
sudo nginx -t

```
