# telegram_auction_bot

Telegram bot that provides auction features via telegram interface

## .env content

- `TOKEN` - telegram bot api key
- `API_ENDPOINT` - api addres (optional if running in docker)
- `PORT` - api port (optional, 8001 by default)
- `ADMIN_CHAT_ID` - telegram chad id to create posts
- `MAIN_CHANNEL_ID` - telegram chat id to send posts

## Run w/ Docker

1. `cd` to project folder
1. create `.env` file
1. dowload or restore databse as `./data_base/sql_app.db`
1. `docker-compose up -d --build`
