import argparse
import logging

from cachspeak import persistence
from cachspeak import settings
from cachspeak import teamspeak
from cachspeak import cachet

parser = argparse.ArgumentParser(description="Send Cachet updates to TeamSpeak")
parser.add_argument('--debug', action='store_true', help='enable logging')
parser.add_argument('--config-path', required=True, help='path of the configuration file')
parser.add_argument('--persist-path', required=True, help='path of the persistence file')

logger = logging.getLogger()


def main(config_path, persist_path, debug=False):
    if debug:
        logger.setLevel(logging.DEBUG)
        logging.info('debug logging enabled')

    settings.config.read(config_path)

    cachet_client = cachet.CachetAPI(endpoint=settings.config.get('Cachet', 'api_url'))

    with persistence.persistent_storage(persist_path) as storage:
        loaded_components = storage.get('last_status', [])
        logging.info('loaded %d saved components', len(loaded_components))

    updates = []
    messages = []
    message_template = settings.config.get('TeamSpeak', 'message_template')
    for update in cachet_client.updated_components(saved_components=loaded_components):
        messages.append(message_template.format(**update))
        updates.append(update)

    teamspeak.send_global_messages(
        messages=messages,
        host=settings.config.get('TeamSpeak', 'host'),
        username=settings.config.get('TeamSpeak', 'login_name'),
        password=settings.config.get('TeamSpeak', 'login_password'),
        bot_nickname=settings.config.get('TeamSpeak', 'bot_nickname'),
        targetmode=settings.config.get('TeamSpeak', 'targetmode'),
        target=settings.config.get('TeamSpeak', 'target')
    )

    with persistence.persistent_storage(persist_path) as storage:
        storage['last_status'] = cachet_client.components


def cli_entry_point(): # pragma: no cover
    args = parser.parse_args()

    main(**args.__dict__)

if __name__ == '__main__': # pragma: no cover
    cli_entry_point()
