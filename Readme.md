# Minting Objects


## Developers

### Create all the necessary environment variables

Create a google cloud api key file. Download it into the env folder of the backend. If that doesnt exist, create it. 

Also download the pem file of the aws ssh key of the ec2 instance. Then:

Add to the environment file *.env* the following entries:
```
POSTGRES_USER=<<enter user>>
POSTGRES_PASSWORD=<<enter password (only utf-8)>>
POSTGRES_DB=<<enter db name>>
PGADMIN_DEFAULT_EMAIL=<<enter random email>>
PGADMIN_DEFAULT_PASSWORD=<<enter random password>>
GOOGLE_CREDENTIAL_FILE=<<name of the json key file from google cloud>>
```

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

### Connecting to ec2 instance

connect to instance:

```
ssh -i "keyfile.pem" ubuntu@ip_address
```

update and upgrade
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

### Other

```
pip list --not-required | awk '{print $1 "==" $2}' > requirements.txt
```

```
docker exec -it backend cat /var/log/apache2/error.log
```

uploads to the flask server can be tested with

```
curl -X POST -F "file=@/home/leonhard/Projects/Hallein/minting-objects-game/backend/img/SocksOrNot.jpg" http://localhost:5000/upload
```

to test the createProductSet route (change the product_set_id!)
```
curl -X POST -H "Content-Type: application/json" \
-d '{"product_set_id": "something", "product_set_display_name": "pumps all the way"}' \                                         
http://localhost:5000/vision/createProductSet
```

to test creation of products:
```
curl -X POST -H "Content-Type: application/json" -d '{"product_id":"squashes", "product_set_id":"veggies", "product_display_name": "something other than pumpkins"}' http://localhost:5000/vision/createProductAndAddToProductSet
```

to test the uploading of an image to a product (change the filename from pumpkin4 to something higher and dont forget to have that file created in you local directory, i.e. not leonhard)

```
curl -X POST -F "file=@/home/leonhard/Projects/Hallein/minting-objects-game/backend/img/pumpkin4.jpg" -F "product_id=pumpkins" http://localhost:5000/upload
```