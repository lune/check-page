#!/usr/bin/env python

import os
import sys
import requests
import datetime

from hashlib import sha512
from twilio.rest import TwilioRestClient

import config

CLIENT = TwilioRestClient(config.TWILO_SID, config.TWILO_AUTH_TOKEN)

def write_hash_to_file(data, path):
    with open(path, 'w') as f:
        f.write(data)

def get_page_hash(url):
    resp = requests.get(url)
    resp.raise_for_status()
    hash_val = sha512(resp.text).hexdigest()
    return hash_val

def get_hash_from_cache(path):
    hash_val = None
    if os.path.exists(path):
        with open(path, 'r') as f:
            hash_val = f.read(-1)
    return hash_val

def send_message(message):
    CLIENT.messages.create(from_=config.TWILO_PHONE_NUMBER, \
            to_=config.USER_PHONE_NUMBER, body_=message)

def send_alive_message():
    send_message('Cron Running well')

if __name__ == '__main__':

    time_now = datetime.datetime.now()
    path = config.CACHE_PATH
    url = config.PAGE_URL

    if time_now.hour == 0 and time_now.minute == 0:
        send_alive_message()
    if len(sys.argv) == 2 and sys.argv[1] == 'clean':
        os.remove(path)

    prev_hash = get_hash_from_cache(path)
    now_hash = get_page_hash(url)

    if prev_hash != now_hash:
        write_hash_to_file(now_hash, path)
        if not prev_hash:
            send_message("Started Clean")
        else:
            send_message("Page Updated")
