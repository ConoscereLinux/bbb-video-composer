# bbb-video-composer
Scripts and utils to compose video recorded in a big blue button session

> **NOTE:** This package use a combination of `makefile`s, python `venv` library and `pip` to 
manage development environment.

## How to install
```shell
# If you have `make` installed
$ make bootstrap

# If you want a more standard approach
$ python -m venv .venv
$ source .venv/bin/activate
(.venv)$ pip install -r requirements.dev.txt --editable .
```

## How to use
```shell
$ source .venv/bin/activate

# Download data from bbb
$ python -m composer download <recording url> --project-name <project id>

# Compose video
$ python -m composer compose <project id> --title <Course title> --relator <relator name> 
```

## Road Map
- [ ] (download) permit usage of only meeting_id instead of full url
- [ ] Add optional output path
- [x] Permit creation of clip
- [x] add routine to create parts for a single video
- [x] move from click to typer