# bbb-video-composer
Scripts and utils to compose video recorded in a big blue button session

## Why this library

## How to install
```shell
# If you have `make` installed
$ make bootstrap
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
- [ ] (download) make option project_name not optional
- [ ] (download) permit usage of only meeting_id instead of full url
- [x] Permit creation of clip
- [ ] Add optional output path
- [ ] add routine to create parts for a single video