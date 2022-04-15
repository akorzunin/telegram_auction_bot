# telegram_auction_bot

Telegram bot that provides auction features via telegram interface

## .env content

- `PWD` -  path to working dir (do not use when starring w/ Docker)
- `ENDPOINT` - api addres for documentation page
- `TOKEN` - telegram bot api key

## Run w/ Docker

1. `cd` to project folder
1. create `.env` file
1. dowload or restore databse as `./data_base/sql_app.db`
1. `sudo ocker-compose  up -d --build`

### Stop Docker

`sudo docker-compose  down`
