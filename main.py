from datetime import datetime
import json
import os
from pathlib import Path

import requests

from activities import get_activity

### Config

CONFIG_PATH = os.environ.get('EA_CONFIG_PATH', Path.joinpath(Path(__file__).resolve().parent, 'config.json'))

Path.joinpath(Path(__file__).resolve().parent, 'config.json')

with open(CONFIG_PATH) as f:
    config_json = json.load(f)

EMBY_DOMAIN = config_json.get('emby_domain', 'http://127.0.0.1')
EMBY_PORT = config_json.get('emby_port', 8096)
EMBY_API_KEY = config_json['emby_api_key']

DISCORD_WEBHOOK_URLS = config_json.get('discord_webhook_urls', [])

ACTIVITY_ITEMS_LIMIT = config_json.get('activity_items_limit', 5)

### Helpers

def report_to_discord(data):
    for discord_webhook_url in DISCORD_WEBHOOK_URLS:
        requests.post(
            url=discord_webhook_url,
            json=data
        )

### ActivityParser

class ActivityParser:
    def __init__(self, domain, port, api_key, limit):
        self.url = '{}:{}/System/ActivityLog/Entries'.format(domain.strip('/'), port)
        self.api_key = api_key
        self.min_date = datetime.utcnow().isoformat()
        self.limit = limit

        self.PARSED_IDS_LIMIT = 100
        self.parsed_ids = []

    def get_activities_data(self):
        response = requests.get(
            url=self.url,
            params={'api_key': self.api_key, 'Limit': self.limit, 'MinDate': '2021-09-23T20:07:24'}  # TODO 'MinDate': self.min_date
            )

        response.raise_for_status()

        return response.json()['Items']
    
    def parse_activities(self):
        activities_data = self.get_activities_data()
        for activity_data in activities_data:
            if activity_data['Id'] in self.parsed_ids:
                continue
            activity = get_activity(activity_data)
            report_to_discord(activity.get_request_body())
            activity.get_request_body()


activity_parser = ActivityParser(EMBY_DOMAIN, EMBY_PORT, EMBY_API_KEY, ACTIVITY_ITEMS_LIMIT)
activity_parser.parse_activities()
