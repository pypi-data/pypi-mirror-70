![](https://telegram.org/img/t_logo.svg?1)
# Telegram Exception Alerts
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Installation

```bash
pip install telegram-exception-alerts
```
or
```bash
poetry add telegram-exception-alerts
```

## Usage

After you initialize the alerter instance you can attach the decorator to any function. If it 
raises an exception information will be send to the chat specified in `chat_id` (don't forget 
that if you want to send notification to a channel you need to prepend that `chat_id` with `-100`).

### Normal initialization

```python
from telegram_exception_alerts import Alerter

alerter = Alerter(bot_token='YOUR_BOT_TOKEN', chat_id='YOUR_CHAT_ID')

@alerter.exception_alert
def some_func_that_can_raise_an_exception():
    raise RuntimeError('this is an exception')
```

### Initialization from environment (recommended)

You can also initialize the alerter from environment variables. **This is the recommended way**
because it will make sure you're not committing sensitive information to the repo.

* `ALERT_BOT_TOKEN` - your bot token
* `ALERT_CHAT_ID` - your chat id to receive notifications

```python
from telegram_exception_alerts import Alerter

alerter = Alerter.from_environment()

@alerter.exception_alert
def some_func_that_can_raise_an_exception():
    raise RuntimeError('this is an exception')
```
