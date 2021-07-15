from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Fetches activities from strava.com'

    def handle(self, *args, **options):
        pass
