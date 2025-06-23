import time

from dotenv import load_dotenv

from dataset.logger import logger
from dataset.models import BBCFeed, GuardianFeed
from dataset.storage_file import FileSystemStore
from storage import DummyStorage
from dataset.storage_mongo import MongoStore

load_dotenv()


def main():
    # initial sources
    feed_sources = {
        'bbc': [
            BBCFeed(
                id='c90ymk1lgrpt',
                topic='online_abuse',
                entries={},
            ),
            BBCFeed(
                id='c4n006pyywdt',
                topic='revenge_porn',
                entries={},
            ),
        ],
        'guardian': [
            GuardianFeed(
                id='technology/children-s-tech',
                topic='children-s-tech',
                entries={},
            ),
            GuardianFeed(
                id='media/social-media',
                topic='social-media',
                entries={},
            ),
            GuardianFeed(
                id='society/online-abuse',
                topic='online-abuse',
                entries={},
            ),
            GuardianFeed(
                id='technology/internet-safety',
                topic='internet-safety',
                entries={},
            ),
            GuardianFeed(
                id='media/ofcom',
                topic='ofcom',
                entries={},
            ),
        ]
    }

    storage = MongoStore()

    # todo: reload previous entries from latest dump

    while True:
        if not storage.ping():
            break
        for source_name, feeds in feed_sources.items():
            for feed in feeds:
                feed.set_storage(storage)
                logger.info(
                    f'started parsing {feed.topic} from source {source_name}')
                feed.parse_rss()

                logger.info(
                    f'finished parsing {feed.topic} from source {source_name}')
                logger.info(f'give some space so we dont get banned...')
                time.sleep(6 * 1)


if __name__ == "__main__":
    main()
