import logging

import ts3


def send_global_messages(messages, host, username, password, bot_nickname=None, targetmode=3, target=1):
    logging.info('sending %d global messages', len(messages))
    if not messages:
        logging.info('no messages to send')
        return
    with ts3.query.TS3Connection(host=host) as ts_connection:
        ts_connection.login(client_login_name=username, client_login_password=password)
        ts_connection.use(sid=1)
        if bot_nickname is not None:
            logging.debug('setting TeamSpeak bot name to %s', bot_nickname)
            ts_connection.clientupdate(client_nickname=bot_nickname)

        for message in messages:
            ts_connection.sendtextmessage(targetmode=targetmode, target=target, msg=message)

    logging.info('sent %d global messages', len(messages))
