import datetime
import json
from dataclasses import dataclass

import feedparser

from dataset.utils import get_hash_hexdigest, timetuple_to_datetime
from storage import Storage
from dataset.logger import logger


@dataclass
class Feed:
    id: str
    topic: str
    entries: dict
    storage: Storage = Storage()
    data_dir: str = "data"
    last_updated: datetime.datetime.timetuple = (datetime.datetime.now(
        datetime.UTC) - datetime.timedelta(hours=24)).timetuple()

    def set_storage(self, storage: Storage):
        logger.info(f'Setting storage to {storage.info}')
        self.storage = storage

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def rss_link(self) -> str:
        raise NotImplementedError

    def parse_rss(self):
        rss = feedparser.parse(self.rss_link)
        logger.info(f'{self.topic}')

        if self.last_updated >= rss.feed.updated_parsed:
            logger.info(
                f'{self.topic} has not been updated since last read, skipping')
            return
        logger.info(
            f'{self.topic} has been updated at {timetuple_to_datetime(rss.feed.updated_parsed)} \
            since last read at  {timetuple_to_datetime(self.last_updated)}')

        logger.info(f'{self.topic} has {len(rss.entries)} entries')
        for entry in rss.entries:
            h = get_hash_hexdigest(entry.link)
            existing_entry = self.entries.get(h)
            if existing_entry:
                # todo: we should also compare updated_at, because entry might get updated since the last read
                # if existing_entry and existing_entry.update_at ==
                # entry.updated_at:
                logger.info(f'entry {h} already exists, skipping')
                continue

            new_entry = Entry(
                id=get_hash_hexdigest(entry.link),
                source=self.name,
                topic=self.topic,
                link=entry.link,
            )
            new_entry = self.storage.store(new_entry)

            self.entries[h] = new_entry
        # todo: we should do some cleanup for memory safety by removing items of
        # which dates are older than the oldest item we read from rss feed.
        self.last_updated = rss.feed.updated_parsed


class BBCFeed(Feed):
    @property
    def name(self) -> str:
        return 'bbc'

    @property
    def rss_link(self) -> str:
        return f'https://feeds.bbci.co.uk/news/topics/{self.id}/rss.xml'


class GuardianFeed(Feed):
    @property
    def name(self) -> str:
        return 'guardian'

    @property
    def rss_link(self) -> str:
        return f'https://www.theguardian.com/{self.id}/rss'


@dataclass
class Entry:
    id: str
    source: str
    topic: str
    link: str
    stored_at: datetime.datetime.timetuple = None

    def to_json(self) -> str:
        return json.dumps(self, default=lambda x: x.__dict__)

    def __str__(self):
        # encoded_link=urllib.parse.quote(self.link, safe='')
        return f'{self.id}, {self.source}, {self.topic}, {self.link}'

