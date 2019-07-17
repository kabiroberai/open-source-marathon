from django.core.management.base import BaseCommand, CommandError
from .scraper.crawler import crawl


class Command(BaseCommand):
    help = 'Scrape the web'

    def handle(self, *args, **options):
        crawl('https://wikipedia.org')
