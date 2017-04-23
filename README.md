#CNTO Cachet to TeamSpeak notification script

This script is used to send a global message on a TeamSpeak server to notify a status change in one or more Cachet components.

##Usage

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

##TODO
 - Change script purpose: notify TeamSpeak only if status on Cachet is different than the status persisted on a given
 file. This would require:
    - An option to update the persistence file (to mantain the actual CNTO usage)
    - A user readable file to allow for custom made default files, at the moment a `pickle` file is used, move to
    JSON or other file conventions