[![Build Status](https://travis-ci.org/CntoDev/cachspeak.svg?branch=master)](https://travis-ci.org/CntoDev/cachspeak)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bd2b276da5fa4c3dbff57a4c80089b60)](https://www.codacy.com/app/CNTODev/cachspeak?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=CntoDev/cachspeak&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/bd2b276da5fa4c3dbff57a4c80089b60)](https://www.codacy.com/app/CNTODev/cachspeak?utm_source=github.com&utm_medium=referral&utm_content=CntoDev/cachspeak&utm_campaign=Badge_Coverage)
[![Requirements Status](https://requires.io/github/CntoDev/cachspeak/requirements.svg?branch=master)](https://requires.io/github/CntoDev/cachspeak/requirements/?branch=master)

# CNTO Cachet to TeamSpeak notification script
This script is used to send a global message on a TeamSpeak server to notify a status change of one or more Cachet components.
Cachspeak shares the same structure of [triscord](https://github.com/CntoDev/triscord), as well as the `persistence` and `settings` modules.

Cachspeak is compatible with Cachet API v1 and TeamSpeak 3.

## Requirements
 - Python 3.5
 
## Installation
`pip install .`

## Usage
Help message is available using `cachspeak -h` or `cachspeak --help`
```
usage: cachspeak [-h] [--debug] --config-path CONFIG_PATH --persist-path
                 PERSIST_PATH

Send Cachet updates to TeamSpeak

optional arguments:
  -h, --help            show this help message and exit
  --debug               enable logging
  --config-path CONFIG_PATH
                        path of the configuration file
  --persist-path PERSIST_PATH
                        path of the persistence file
```

## Configuration
A configuration file following a ini-like syntax is required for connecting to Cachet and TeamSpeak services, an example is provided with the `cachspeak.ini.dist` file.

**Note**: it is *highly* recommended that the machine running *cachspeak* is whitelisted on TeamSpeak server, otherwise a flood-ban is very likely to happen. Refer to ServerQuery documentation to add an address to the whitelist.

### TeamSpeak notifications configuration
 - The message sent to TeamSpeak can be customized with syntax highlighting (refer to TeamSpeak messaging documentation) and it is possible to show more information about every updated component: several placeholders are available, each one will be replaced with the actual component data. A placeholder must be enclosed by brackets in order to be used.The available placeholders are: `id`, `name`, `status`, `status_name`, `created_at`, `updated_at`, `deleted_at`.
 - It is possible to specify the messages recipient (i.e. a single client, a whole channel, etc) by adjusting the `targetmode` and `target` options in the configuration file. Refer to ServerQuery documentation for details about values.
 - The bot name (shown in blue at the beginning of each global message) can be customized by adjusting the value of `bot_nickname` in the configuration file.
