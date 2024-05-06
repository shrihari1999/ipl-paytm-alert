import requests, smtplib, ssl, urllib.parse, os
from time import sleep
from line_notify import LineNotify
from exponent_server_sdk import DeviceNotRegisteredError, PushClient, PushMessage, PushServerError, PushTicketError
from requests.exceptions import ConnectionError, HTTPError

# dont run if file has value True
with open(os.path.join(os.path.dirname(__file__), 'paytm.txt'), 'r') as f:
    if f.read() == 'True':
        exit()

def send_mails(search_term, match_url):
    sender_email = '' # TODO: Enter sender email
    password = '' # TODO: Enter sender email password
    port = 587  # For SSL
    
    recipients = [] # TODO: Enter recipient emails
    message = f"""\
    Subject: IPL {search_term} tickets available!

    {match_url}"""

    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        for recipient in recipients:
            server.sendmail(sender_email, recipient, message)

def send_alerts(search_term):
    expo_tokens = [] # TODO: Enter expo tokens
    push_message = PushMessage(to=expo_push_token, title=f"IPL {search_term} tickets available!", body=f"IPL {search_term} tickets available!")
    for expo_push_token in expo_tokens:
        try:
            response = PushClient().publish(push_message)
            try:
                # This call raises errors so we can handle them with normal exception flows.
                response.validate_response()
            except DeviceNotRegisteredError:
                print('Device not registered')
            except PushTicketError as exc:
                # Encountered some other per-notification error.
                print(exc.push_response._asdict())
        except PushServerError as exc:
            print(exc.errors)
            print(exc.response_data)
        except (ConnectionError, HTTPError) as exc:
            print('Connection or HTTP error')
    pass

def send_line_alerts(search_term, match_url):
    message = f"IPL {search_term} tickets available!\n\n{match_url}"
    notify = LineNotify('') # TODO: Enter LINE access token
    notify.send(message)

url = "https://1bfwmgchj2-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)%3B%20react%20(16.8.6)%3B%20react-instantsearch%20(5.7.0)%3B%20JS%20Helper%20(2.28.1)&x-algolia-application-id=1BFWMGCHJ2&x-algolia-api-key=d96f92a248e8dd9aa36d08c78678a956"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "content-type": "application/x-www-form-urlencoded",
    "referrer": "https://insider.in/",
}
keywords = ['match 59 ', 'chennai']
search_term = ' '.join(keywords)
query = urllib.parse.quote(search_term)
data = {
    'requests': [
        {'indexName': 'events', 'params': f"query={query}&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&filters=endTime%20%3E%201680114608%20AND%20(NOT%20tagids%3A5836dfe53a3e6042078e2bc6%20)%20%20AND%20(%20tagids%3A5e9eacd93dc0550988a466dd%3Cscore%3D1%3E%20OR%20NOT%20tagids%3A5e9eacd93dc0550988a466dd%3Cscore%3D0%3E%20)&facets=%5B%5D&tagFilters="}
    ]
}

response = requests.post(url, headers=headers, json=data).json()
for hit in response['results'][0]['hits']:
    hit_name = hit['name'].lower()
    if all([keyword in hit_name for keyword in keywords]) and hit['event_state'] == 'available':
        match_url = f"https://insider.in/{hit['slug']}/event"
        send_mails(search_term, match_url)
        # write True to file
        with open(os.path.join(os.path.dirname(__file__), 'paytm.txt'), 'w') as f:
            f.write('True')
        while True:
            send_alerts(search_term)
            send_line_alerts(search_term, match_url)
            sleep(10)
