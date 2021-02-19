# ReachOut Scraper

Scraping right-wing incidents in Berlin, Germany as monitored by the NGO [ReachOut](https://www.reachoutberlin.de/).

-   Website: <https://www.reachoutberlin.de/de/chronik>
-   Data: <https://morph.io/rechtegewalt/reachout-scraper>

## Usage

For local development:

-   Install [poetry](https://python-poetry.org/)
-   `poetry install`
-   `poetry run python scraper.py`

For Morph:

-   `poetry export -f requirements.txt --output requirements.txt`
-   commit the `requirements.txt`
-   modify `runtime.txt`

## Morph

This is scraper runs on [morph.io](https://morph.io). To get started [see the documentation](https://morph.io/documentation).

## License

MIT
