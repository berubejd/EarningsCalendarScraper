# Earnings Calendar Scraper

This is a small command line tool which uses [Requests-HTML](https://docs.python-requests.org/projects/requests-html/) in order to query a web page and scrape some information after the JavaScript has been rendered.

## Quickstart

There is help included but below demonstrates the applications functionality:

``` shell
$ python earnings.py
usage: earnings [-h] [--verbose] symbol
earnings: error: the following arguments are required: symbol

$ python earnings.py --verbose tsla
Fetching data for tsla...

Report Date: Apr 26, 2021
Fiscal Quarter: 2021 (Q1)

$ python earnings.py goog
2021-04-27|2021 (Q1)
```

## Requirements

There is a requirements.txt available which details necessary libraries not included in standard Python.  Additionally, the program may require that you install additional system packages such as chromium-browser and libxss1 in Ubuntu.
