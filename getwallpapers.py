#!/usr/bin/env python3

import sys
import requests

from bs4 import BeautifulSoup


class Month:
    """
    Represents wallpaper month.

    Example:
    Month(2017, 4) means wallpapers for April 2017.
    Article was published in March 2017.
    """

    def __init__(self, year: int, month: int):
        if not 1 <= month <= 12:
            raise ValueError(
                "Month must be between 1 and 12"
            )

        self.year = year
        self.month = month

    @property
    def article_year(self) -> int:
        if self.month == 1:
            return self.year - 1

        return self.year

    @property
    def article_month(self) -> int:
        if self.month == 1:
            return 12

        return self.month - 1


def find_article_url(
        category_url: str,
        month: Month,
        max_pages: int = 100,  # Limit the number of pages to check
) -> str | None:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for page in range(1, max_pages + 1):
        if page == 1:
            url = category_url
        else:
            url = f"{category_url}/page/{page}/"

        response = requests.get(
            url,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )
        articles = soup.find_all(
            "article",
            class_="article--post"
        )

        for article in articles:
            time = article.find("time")

            if not time:
                continue

            date = time.get("datetime")

            if not date:
                continue

            published_year = int(date[:4])
            published_month = int(date[5:7])

            if (
                published_year == month.article_year
                and published_month == month.article_month
            ):
                title = article.find(
                    "h2",
                    class_="article--post__title"
                )

                if title:
                    link = title.find(
                        "a",
                        href=True
                    )

                    if link:
                        return (
                            "https://www.smashingmagazine.com"
                            + link["href"]
                        )
    return None


def parse_arguments() -> tuple[Month, str]:
    if len(sys.argv) != 3:
        print(
            "Usage: ./getwallpapers.py MMYYYY resolution"
        )
        sys.exit(1)

    month_year = sys.argv[1]
    resolution = sys.argv[2]

    month = int(month_year[:2])
    year = int(month_year[2:])

    return Month(year, month), resolution


if __name__ == "__main__":
    wallpaper_month, resolution = parse_arguments()

    article_url = find_article_url(
        "https://www.smashingmagazine.com/categories/wallpapers",
        wallpaper_month
    )

    print(article_url)
