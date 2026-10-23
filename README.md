This is a telegram bot that uses wikipedia's API to look up pages, similar to users search. It than outputs them as a single message containing links to found pages.

# Initial Setup

Install requirements
```
python -m pip install -r requirements.txt
```
Create a .env file (either manually or with ```cp .env.example .env```)
Set your ```TELEGRAM_BOT_KEY``` in the .env

Start bot with ```python main.py```