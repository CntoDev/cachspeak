import logging

import ts3


def send_global_messages(messages, host, username, password):
    logging.info('sending %d global messages', len(messages))
    if not messages:
        logging.info('no messages to send')
        return
    with ts3.query.TS3Connection(host=host) as ts_connection:
        ts_connection.login(client_login_name=username, client_login_password=password)
        ts_connection.use(sid=1)

        for message in messages:
            ts_connection.gm(msg=message)

    logging.info('sent %d global messages', len(messages))
