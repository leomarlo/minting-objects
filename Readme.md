# Minting Objects


## Developers

### Install the packages

```
cd backend && python3 -m venv .venv
```

Then activate that environment. In windows its different than in linux or mac-OS. in any case in the latter it should be like:

```
source .venv/bin/activate
```

And then 

```
pip install -r requirements.txt
```



Add to the environment file *.env* the following entries:
```
POSTGRES_USER=<<enter user>>
POSTGRES_PASSWORD=<<enter password (only utf-8)>>
POSTGRES_DB=<<enter db name>>
PGADMIN_DEFAULT_EMAIL=<<enter random email>>
PGADMIN_DEFAULT_PASSWORD=<<enter random password>>
```


```
pip list --not-required | awk '{print $1 "==" $2}' > requirements.txt
```

```
docker exec -it backend cat /var/log/apache2/error.log
```

connect to instance:

```
ssh -i "keyfile.pem" ubuntu@ip_address
```

update and upgrad
```
sudo apt update
sudo apt upgrade -y
```

reboot instance

```
sudo apt install docker.io git -y
```

```
sudo systemctl start docker
sudo systemctl enable docker
```

```
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

```
sudo chmod +x /usr/local/bin/docker-compose
```

