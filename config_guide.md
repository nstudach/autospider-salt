# Spiderweb creates a web of spiders

Spiderweb is a tool for spawning webs of pathspider
workers. It uses SaltStack as a backend.

Usage: `spiderweb path/to/config/file.json`

## config file

The config file should be JSON formated, and contain the following:

```
{
    "pathspider_args": "Arguments for pathspider",
    "input_file": "List of servers to probe with pathspider as .ndjson file",
    "minions":
        {"do-sfo1-512": 0,
         "do-lon1-512": 1
        },
    "when_done": "destroy",
}
```

**pathspider_args:** The argument string to be passed to PathSpider.
Before it is passed on to PathSpider, it will be processed as follows:
`pathspider_args = pathspider_args.format(**__grains__)`, where
`__grains__` is the pathspider grains dictionary.

**input_file:** The path to the file to be used for pathspiders measurments as ndjson.

**minion:** An object defining for every listed Salt Cloud profile
how many minions should be spawned. Format: string:integer

**when_done:** Action to execute when PathSpider is done. Currently
only `destroy` and `None` are supported

All of the members of the root object will be available as grains on the minions
