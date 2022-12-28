FaDiSma
=======

Boilerplate code to build discord bots 

Packages
------------

- FastAPI - for the webserver, and the API
- Disnake - for the discord bot
- Prisma - for the database

New project
------------

- Clone the repo
- Create a virtual environment
- Install the requirements
- Create .env files 
- Run the migrations
- Run the bot 

### Clone the repo

```bash
git clone --depth 1 https://github.com/yatochka-dev/discord-bot-boilerplate <YOUR_PROJECT_NAME>

cd <YOUR_PROJECT_NAME>
```


### Create a virtual environment

```bash
python -m venv <YOUR_VENV_NAME>
```

### Install the requirements

```bash
pip install -r requirements.txt
```

### Create .env files

- Create a .env.development file in the root directory and fill it like **_.env.example_**
- Create a .env.production file in the root directory and fill it like _**.env.example**_

#### .env.development 
- this file will be used, when your bot is running in testing mode

#### .env.production
- this file will be used, when your bot is running in production mode

### Run the migrations

```bash
prisma generate

prisma migrate dev --name init
```

### Run the bot

```bash
python -m uvicorn main:app --reload
```

## Bot configuration 
In <YOUR_PROJECT_NAME>.app.bot.py file you can find class named 
**AppSettings**. This class contains all the settings for your bot.
Switching between testing and production mode is done by changing the **TESTING** variable.




