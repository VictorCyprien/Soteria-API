# Soteria-API

Soteria-API is a REST API that lets you view and manage the equipment of one or more Destiny 2 guardians by interacting with Bungie's API.

## Requirements

- Windows or Linux
- Python (with pip)

## How to install ?

1. Open a new terminal
2. Clone this repository
    
    - With HTTPS :
        - `git clone https://github.com/VictorCyprien/soteria-api.git`

    - With SSH :
        - `git clone git@github.com:VictorCyprien/soteria-api.git`

3. Move to the project

    - `cd /soteria-api`


4. Create a new virtual environnement

    - `virtualenv venv`
    
    ___Note___ : To install virtualenv, please use `pip install virtualenv`

5. Activate your new virtual environnement

    - Windows : `source venv/Scripts/activate`

    - Linux : `source venv/bin/activate`

6. Install dependencies

    - `make install`
    
    ___Note___ : If your system can't execute the command `make`, do this instead :
    - `pip install -r requirements.txt`
    - `pip install -r requirements.dev.txt`
    - `pip install -r requirements.aiobungie.txt`
    - `pip install -e ./`


7. Setup environnements variable

You need to setup some environnements variables in order to make the API to work<br>
- First, create a file `.env` at the root of the project<br>
- Then, set those variables :<br>

    - _BUNGIE_API_KEY_ : The API-Key used to interact with Bungie's API
    - _BUNGIE_API_CLIENT_ID_ : The ID of your client
    - _BUNGIE_API_CLIENT_SECRET_ : The password of your client

___Note___ : You can have your own credentials with this official link : https://www.bungie.net/en/Application


8. Launch the API

To launch the API, use this command :
- `make run`

___Note___ : If your system can't execute the command `make`, do this instead :
- `python run.py`


__IMPORTANT__ : You need to set certifications to start the API. For this, create a folder 'certs' at the root of the projet and generate the following certificates :

- certificate.pem
- crs.pem
- key.pem


### Generate swagger

To generate the swagger, launch the API and go to this link : 
https://localhost:5000/api/docs/swagger.json

This will generate the swagger in JSON and YAML
You can see the swagger on this website : https://editor.swagger.io/
Just copy/paste the content of the swagger and you'll see the architecture of the API
