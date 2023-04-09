# ipl-paytm-alert
Send alerts if tickets are open for an IPL match on Paytm Insider.

## Setup

### Search keywords
Update array "keywords" with any keywords that will be present in the title. The first result is considered. I recommend only updating the match number and team name without modifying anything else in the existing array.

### Email alerts

Email alert is only sent once after match is found. Paytm match link is included in body.

1. Enter sender_email and password values
2. Enter recipients in recipients array

### Push notifications

Push notifications are sent every 10 seconds

1. To get Expo push token, refer to https://docs.expo.dev/versions/latest/sdk/notifications/#getexpopushtokenasyncoptions. You need to know your way around React and Expo to easily get this
2. Enter the push tokens in expo_tokens array

## Run
As a prerequisite, make sure you have python3.7, pip and pipenv installed.

In the root directory where Pipfile is present, run
```
pipenv shell
```

Install required packages
```
pipenv install
```

Setup cron job
```
* * * * * /path/to/venv-python /path/to/paytm.py >> /path/to/paytm.log 2>&1
```

Example:
```
* * * * * /home/ubuntu/.local/share/virtualenvs/paytm-KhZiLQF8/bin/python3.7 /home/ubuntu/paytm/paytm.py >> /home/ubuntu/paytm/paytm.log 2>&1
```


