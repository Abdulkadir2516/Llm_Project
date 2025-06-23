import os
import sys
import pathlib

from discord import SyncWebhook


class Discord:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    webhook_url: str

    def send(self, message: str, f: pathlib.Path):
        webhook = SyncWebhook.from_url(self.webhook_url)
        webhook.send(message, file=f)


def get_new_discord():
    discord_webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if discord_webhook_url is None:
        sys.exit("please set env variable DISCORD_WEBHOOK_URL")
    return Discord(discord_webhook_url)
