# "Docker for Mac" Download Links

Inspired by [docker/for-mac#1120](https://github.com/docker/for-mac/issues/1120).

## Usage

Install the python dependencies:

```
virtualenv -p python3 venv
./venv/bin/pip install -r requirements.txt
```

And execute the scraper:

```
> ./venv/bin/python3 scrape.py --help
usage: scrape.py [-h] [--limit LIMIT] [--out OUT] {amd64,arm64}

Scrape for Docker for Mac architecture release download links

positional arguments:
  {amd64,arm64}

optional arguments:
  -h, --help     show this help message and exit
  --limit LIMIT  Maximum number of builds to scan for
  --out OUT      JSON file to output build info
```

## Example

Scrape for the latest 1000 builds of the amd64 architecture:

```
> ./venv/bin/python3 scrape.py amd64 --out amd64.json --limit=1000
```
