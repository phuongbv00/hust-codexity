# DATA COLLECTOR 🤘🤘🤘

This is a microservice for collecting data from Stackoverflow and providing APIs to get data.

This microservice has 2 api:

 1. `[GET]: http://{domain:port}/fetch_code` : Trigger collecting data from Stackoverflow (call api.stackexchange.com) to get questions and answers. After getting data, save them at `stackoverflow_c_code.json`.
 2. `[GET]: http://{domain:port}/get_saved_code`: Get and return data from  `stackoverflow_c_code.json` . If file `stackoverflow_c_code.json` does not exist or empty, using file `sample-data.json` instead.

# How to install
Follow this guide to run this microservice 

## Prerequisite
 1. Installed Docker: https://docs.docker.com/desktop/setup/install/mac-install/
 2. Create `.env` file with content like content of `.env.development`, then enter local port. Sample `PORT=8080`

## Run current microservice
At `data-collector` folder, run commands bellow:

    docker-compose up --build
