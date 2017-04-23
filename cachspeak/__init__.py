import argparse
import json
import logging

import ts3
import cachetclient.cachet as cachet

from . import persistence
from . import settings

COMPONENT_FIELDS = {'id', 'name', 'status', 'created_at', 'updated_at', 'deleted_at', 'status_name'}

parser = argparse.ArgumentParser(description="Send Cachet updates to TeamSpeak")
parser.add_argument('--debug', action='store_true', help='enable logging')
parser.add_argument('--config-path', required=True, help='path of the configuration file')
parser.add_argument('--persist-path', required=True, help='path of the persistence file')

logger = logging.getLogger()


def retrieve_cachet_components(base_endpoint):
    request = cachet.Components(endpoint=base_endpoint)
    response = json.loads(request.get())
    components = tuple(response['data'])

    for comp in components:
        for key, value in comp.copy().items():
            if key not in COMPONENT_FIELDS:
                del comp[key]

    return components


def get_updated_components(saved, new):
    updated_status = []

    for new_component in new:
        matching_saved_components = list(filter(lambda saved_component: saved_component['id'] == new_component['id'], saved))

        if not matching_saved_components:
            updated_status.append(new_component)
        else:
            matching_saved_component = matching_saved_components[0]
            if new_component['status'] != matching_saved_component['status']:
                updated_status.append(new_component)

    return updated_status


def notify_ts(ts_connection, status_updates, message_template):
    if not status_updates:
        logging.info('no TeamSpeak notifications sent')
    else:
        for update in status_updates:
            try:
                status_message = message_template.format(**update)
                ts_connection.gm(msg=status_message)
            except KeyError:
                logging.error('message template contains invalid placeholders, see documentation for reference')
                raise KeyError('TeamSpeak message template contains invalid placeholders')
        logging.info('TeamSpeak update global messages sent')


def main(config_path, persist_path, debug=False):
    if debug:
        logger.setLevel(logging.DEBUG)
        logging.info('debug logging enabled')

    settings.config.read(config_path)

    new_status = retrieve_cachet_components(base_endpoint=settings.config.get('Cachet', 'api_endpoint'))
    logging.info('retrieved status of %d Cachet components', len(new_status))

    with persistence.persistent_storage(persist_path) as storage:
        if 'saved_status' in storage:
            loaded_status = storage['saved_status']
            saved_status = tuple(dict(t) for t in set([tuple(d.items()) for d in loaded_status]))
            logging.info('retrieve saved status of %d components', len(saved_status))
        else:
            saved_status = ()

    updated_status = get_updated_components(saved_status, new_status)
    logging.info('%d components were updated', len(updated_status))

    with ts3.query.TS3Connection(host=settings.config.get('TeamSpeak', 'host')) as ts_connection:
        ts_connection.login(
            client_login_name=settings.config.get('TeamSpeak', 'login_name'),
            client_login_password=settings.config.get('TeamSpeak', 'login_password'))
        ts_connection.use(sid=1)
        notify_ts(
            ts_connection=ts_connection,
            status_updates=updated_status,
            message_template=settings.config.get('TeamSpeak', 'message_template')
        )

    with persistence.persistent_storage(persist_path) as storage:
        storage['saved_status'] = updated_status


def cli_entry_point():
    args = parser.parse_args()

    main(**args.__dict__)

if __name__ == '__main__':
    cli_entry_point()
