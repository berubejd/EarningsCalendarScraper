import argparse
import sys
from datetime import datetime
from time import sleep
from typing import Optional

import requests
import requests_html
from requests.models import Response


def main():
    verbose: bool
    symbol: str
    verbose, symbol = process_args()

    url: str = f"https://www.tipranks.com/stocks/{symbol}/earnings-calendar"

    if verbose:
        print(f"Fetching data for {symbol}...\n")

    scraped_data: tuple = process_page(url, verbose)

    if scraped_data:
        if verbose:
            output: str = (
                f"Report Date: {scraped_data[0]}\n"
                f"Fiscal Quarter: {scraped_data[1]}\n"
            )
        else:
            dt: datetime = datetime.strptime(scraped_data[0], "%b %d, %Y")
            output: str = f"{dt.date().isoformat()}|{scraped_data[1]}"
        print(output)
    else:
        if verbose:
            print("No data available")

        sys.exit(1)


def process_args() -> tuple:
    parser = argparse.ArgumentParser(
        prog="earnings", description="Return the latest earnings date"
    )
    parser.add_argument(
        "--verbose", help="Provide verbose output", action="store_true", default=False
    )
    parser.add_argument("symbol", help="The stock symbol to request data for")
    args = parser.parse_args()

    verbose: bool = args.verbose
    symbol: str = args.symbol

    return verbose, symbol


def get_page(url: str) -> Response:
    headers: str = {"User-Agent": requests_html.user_agent()}

    with requests_html.HTMLSession() as s:
        resp: Response = s.get(url, headers=headers)

        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            return None

        return resp


def process_page(url: str, verbose: bool) -> Optional[tuple]:
    count = 0
    max_retries = 3

    while count < max_retries:
        # Checking the count rather than sleep on the final loop check when we are just going to exit
        if not count == 0:
            sleep(5)

        try:
            page = get_page(url)
            page.html.render(sleep=2)
        except:
            if verbose:
                print("An error occurred during page loading and processing")

            return None

        row = page.html.find(".rt-tbody .rt-tr", first=True)

        if row:
            # There is row data so continue processing
            break

        if page.html.find(
            ".client-components-stock-research-earings-style__EarningsHistoryTable span",
            containing="Currently, no data available",
        ):
            # This symbol doesn't provide earnings calendar data so exit rather than try to reload
            if verbose:
                print(f"Notice: No earnings calendar available for this stock symbol")

            return None

        if verbose:
            print(f"Sleeping... ({count + 1})")

        count += 1

    else:
        # Page loading has failed to return the row afer 'max_retries'
        return None

    data = row.find(".rt-td")

    return data[0].text, data[1].text


if __name__ == "__main__":
    main()
