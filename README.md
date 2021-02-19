# aas-todesopfer-scraper

-   Website: <https://www.amadeu-antonio-stiftung.de/todesopfer-rechter-gewalt/>
-   Data: <https://morph.io/rechtegewalt/aas-todesopfer-scraper>

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
