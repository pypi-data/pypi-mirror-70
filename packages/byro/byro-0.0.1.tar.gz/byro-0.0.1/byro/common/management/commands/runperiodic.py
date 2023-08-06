from django.core.management.base import BaseCommand

from byro.common.signals import periodic_task


class Command(BaseCommand):
    help = "Run periodic tasks"

    def handle(self, *args, **options):
        periodic_task.send(self)
