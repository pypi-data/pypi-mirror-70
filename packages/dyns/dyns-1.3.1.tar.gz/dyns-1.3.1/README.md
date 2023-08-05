# dynsctl

Command line tool to interact with `dyns` API

## Install

`pip install -U dyns`

## Usage

```
Usage: dynsctl [OPTIONS] COMMAND [ARGS]...

Options:
  -A, --api-endpoint TEXT  dyns API endpoint, defaults to
                           http://127.0.0.1:8053

  --help                   Show this message and exit.

Commands:
  add
  delete
  ls
  version
```

Set default API endpoint in `$HOME/.dynsrc`

```
[dynsctl]
api_endpoint = "http://10.20.30.1:8080"
```
