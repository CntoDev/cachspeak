# CNTO Cachet to TeamSpeak notification script
This script is used to send a global message on a TeamSpeak server to notify a status change of one or more Cachet components.

## Requirements
 - Python 3.5
 
## Installation
`pip install cachspeak`

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
A configuration file following a ini-like syntax is required for connecting to Cachet and TeamSpeak services, an example is provided with the `cachspeak.ini.dist`file.

The message sent to TeamSpeak can be customized with syntax highlighting (refer to TeamSpeak messaging documentation) and it is possible to show more information about every updated component: several placeholders are available, each one will be replaced with the actual component data. A placeholder must be enclosed by brackets in order to be used.
The available placeholders are: `id`, `name`, `status`, `status_name`, `created_at`, `updated_at`, `deleted_at`.

**Note**: it is *highly* recommended that the machine running *cachspeak* is whitelisted on TeamSpeak server, otherwise a flood-ban is very likely to happen. Refer to ServerQuery documentation to add an address to the whitelist.
