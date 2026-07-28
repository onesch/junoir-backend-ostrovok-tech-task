#!/usr/bin/env python3

import sys
import requests
import calendar
import re
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime

from logger import logger
from arguments import parse_arguments


class Month:
    """
    Represents wallpaper month.

    Example:
    Month(2017, 4) means wallpapers for April 2017.
    Article was published in March 2017.
    """

    def __init__(self, year: int, month: int):
        if not 1 <= month <= 12:
            raise ValueError("Month must be between 1 and 12")

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


def find_wallpaper_urls(
    article_url: str,
    month: Month,
    resolutions: list[str],
) -> list[str]:
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(
        article_url,
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    wallpapers = []

    resolution_pattern = "|".join(map(re.escape, resolutions))

    month_full = calendar.month_name[month.month].lower()
    month_short = calendar.month_abbr[month.month].lower()

    start_url = (
        rf"https?://(www\.)?smashingmagazine\.com/files/wallpapers/"
        rf"({month_full}|{month_short})-"
        rf"{str(month.year)[-2:]}/"
    )

    pattern = re.compile(
        rf"^{start_url}"
        rf".*-(cal|nocal)-({resolution_pattern})\.[a-zA-Z0-9]+$"
    )

    links = soup.find_all("a", href=True)

    for link in links:
        href = link["href"]

        if pattern.match(href):
            if href not in wallpapers:
                wallpapers.append(href)

    logger.info(f"Found wallpapers: {len(wallpapers)}")

    return wallpapers


def find_article_url(
    category_url: str,
    month: Month,
    max_pages: int = 100,
) -> str | None:
    category_url = category_url.rstrip("/")

    headers = {"User-Agent": "Mozilla/5.0"}

    target_year = month.article_year
    target_month = month.article_month

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

        if response.status_code == 404:
            break

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.find_all("article", class_="article--post")

        for article in articles:

            time = article.find("time", class_="article--post__time")

            if not time:
                continue

            date = time.get("datetime")
            date_obj = datetime.strptime(date, "%Y-%m-%d")

            if not date:
                continue

            published_year = date_obj.year
            published_month = date_obj.month

            if published_year < target_year:
                return None

            if published_year > target_year:
                continue

            if published_month != target_month:
                continue

            title = article.find("h2", class_="article--post__title")

            if not title:
                continue

            link = title.find("a", href=True)

            if not link:
                continue

            article_url = "https://www.smashingmagazine.com" + link["href"]

            logger.info(f"Found article: {article_url}")

            return article_url

    return None


def download_wallpapers(
    wallpaper_urls: list[str],
    year: int,
    month: int,
    output_dir: str = "wallpapers",
) -> None:

    save_dir = Path(output_dir) / str(year) / f"{month:02d}"

    save_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    headers = {"User-Agent": "Mozilla/5.0"}

    for url in wallpaper_urls:

        filename = Path(urlparse(url).path).name

        filepath = save_dir / filename

        if filepath.exists():
            logger.info(f"Already exists: {filepath}")
            continue

        response = requests.get(
            url,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        filepath.write_bytes(response.content)

        logger.info(f"Downloaded: {filepath}")


if __name__ == "__main__":
    year, month, resolution = parse_arguments()

    wallpaper_month = Month(year, month)

    article_url = find_article_url(
        "https://www.smashingmagazine.com/category/wallpapers", wallpaper_month
    )

    if article_url is None:
        logger.error("Wallpaper article not found.")
        sys.exit(1)

    wallpaper_urls = find_wallpaper_urls(
        article_url,
        wallpaper_month,
        [resolution],
    )

    download_wallpapers(
        wallpaper_urls,
        year,
        month,
    )
