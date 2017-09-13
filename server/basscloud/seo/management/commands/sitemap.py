from django.core.management.base import BaseCommand, CommandError
from basscloud.catalog.models import Project


class Command(BaseCommand):
    help = 'Generates sitemap in simple text format'

    def handle(self, *args, **options):
        site = 'https://basscloud.net'
        for project in Project.objects.filter(public=True):
            self.stdout.write(site+'/project/'+project.id)
